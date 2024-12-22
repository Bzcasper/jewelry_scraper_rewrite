import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
from typing import Optional, Dict
from utils.proxy_manager import ProxyManager
from utils.rate_limiter import AdaptiveRateLimiter

class ScraperMiddleware:
    """Middleware for handling request/response and resource management"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.proxy_manager = ProxyManager()
        self.rate_limiter = AdaptiveRateLimiter()
        self.session: Optional[aiohttp.ClientSession] = None

    async def fetch_page(self, url: str, platform: str) -> Optional[str]:
        """Fetch page content with rate limiting and optional proxy rotation"""
        await self.rate_limiter.wait(platform)
        proxy = await self.proxy_manager.get_proxy()

        try:
            if not self.session:
                self.session = aiohttp.ClientSession()

            async with self.session.get(
                url,
                proxy=proxy.url if proxy else None,
                timeout=30
            ) as response:
                if response.status == 200:
                    self.rate_limiter.update_success_rate(True)
                    return await response.text()
                elif response.status == 403:
                    self.logger.warning(f"Access blocked for {url}")
                    if proxy:
                        await self.proxy_manager.report_failure(proxy)
                    self.rate_limiter.update_success_rate(False)
                    return None
                else:
                    self.logger.warning(f"Unexpected status {response.status} for {url}")

        except Exception as e:
            self.logger.error(f"Failed to fetch page {url}: {e}")
            if proxy:
                await self.proxy_manager.report_failure(proxy)
            self.rate_limiter.update_success_rate(False)
            return None

    async def process_response(self, html: str, platform: str) -> Optional[Dict]:
        """Process and extract structured data from HTML response"""
        try:
            soup = BeautifulSoup(html, 'html.parser')

            # Check for anti-bot mechanisms
            if self._is_blocked(soup, platform):
                self.logger.warning(f"Anti-bot mechanisms detected on {platform}")
                return None

            # Extract structured data
            structured_data = self._extract_structured_data(soup)
            return structured_data

        except Exception as e:
            self.logger.error(f"Failed to process response: {e}")
            return None

    def _is_blocked(self, soup: BeautifulSoup, platform: str) -> bool:
        """Check if response contains anti-bot indications"""
        if platform == 'amazon':
            return any(term in soup.get_text().lower() for term in ['robot', 'captcha', 'verify'])
        elif platform == 'ebay':
            return any(term in soup.get_text().lower() for term in ['security measure', 'verify'])
        return False

    def _extract_structured_data(self, soup: BeautifulSoup) -> Optional[Dict]:
        """Extract structured data using JSON-LD or other schemas"""
        try:
            for script in soup.find_all('script', type='application/ld+json'):
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict) and data.get('@type') in ['Product', 'Offer']:
                        return data
                except json.JSONDecodeError:
                    continue
            return None

        except Exception as e:
            self.logger.error(f"Error extracting structured data: {e}")
            return None

    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
            self.session = None
