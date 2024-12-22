import asyncio
from typing import Optional, Dict, List
from dataclasses import dataclass, field
import logging
import random

@dataclass
class Proxy:
    """Represents a proxy configuration"""
    host: str
    port: int
    protocol: str = "http"
    username: Optional[str] = None
    password: Optional[str] = None
    failures: int = 0
    success_rate: float = 1.0  # Defaults to 100% success rate

    def url(self) -> str:
        """Generate the proxy URL"""
        auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
        return f"{self.protocol}://{auth}{self.host}:{self.port}"

class ProxyManager:
    """Manages proxies and handles rotation, failures, and success tracking"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.proxies: List[Proxy] = []
        self.lock = asyncio.Lock()

    def add_proxy(self, host: str, port: int, protocol: str = "http", username: Optional[str] = None, password: Optional[str] = None):
        """Add a new proxy to the pool"""
        proxy = Proxy(host=host, port=port, protocol=protocol, username=username, password=password)
        self.proxies.append(proxy)
        self.logger.info(f"Added proxy: {proxy.url()}")

    async def get_proxy(self) -> Optional[Proxy]:
        """Get a proxy with the highest success rate, or None if no proxies available"""
        async with self.lock:
            if not self.proxies:
                self.logger.warning("No proxies available.")
                return None

            self.proxies.sort(key=lambda proxy: proxy.success_rate, reverse=True)
            selected_proxy = random.choice(self.proxies[:3])  # Choose from top 3 highest success rates
            self.logger.info(f"Selected proxy: {selected_proxy.url()}")
            return selected_proxy

    async def report_failure(self, proxy: Proxy):
        """Report a failure for a proxy"""
        async with self.lock:
            proxy.failures += 1
            proxy.success_rate = max(0.0, proxy.success_rate - 0.1)  # Decrease success rate
            self.logger.warning(f"Proxy failure reported: {proxy.url()} | Failures: {proxy.failures}")

    async def report_success(self, proxy: Proxy):
        """Report a success for a proxy"""
        async with self.lock:
            proxy.success_rate = min(1.0, proxy.success_rate + 0.05)  # Increase success rate
            self.logger.info(f"Proxy success reported: {proxy.url()} | Success rate: {proxy.success_rate:.2f}")

    async def release_proxy(self, proxy: Proxy):
        """Release the proxy back to the pool"""
        async with self.lock:
            self.logger.info(f"Proxy released: {proxy.url()}")

    async def cleanup(self):
        """Clean up proxies with excessive failures"""
        async with self.lock:
            threshold = 5
            self.proxies = [proxy for proxy in self.proxies if proxy.failures < threshold]
            self.logger.info(f"Cleaned up proxies. Remaining proxies: {len(self.proxies)}")
# backend/app/utils/proxy_manager.py
from typing import Optional, List
import aiohttp
import asyncio
import random
from ..config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)

class Proxy:
    def __init__(self, url: str):
        self.url = url
        self.fails = 0
        self.last_used = 0

class ProxyManager:
    """"""Manage and rotate proxies""""""
    
    def __init__(self):
        self.proxies: List[Proxy] = []
        self.current_index = 0
        self._lock = asyncio.Lock()
        self._initialized = False

    async def initialize(self):
        """"""Load proxies from configuration""""""
        if self._initialized:
            return
            
        try:
            with open(settings.PROXY_LIST_PATH, 'r') as f:
                proxy_urls = f.read().splitlines()
                
            self.proxies = [Proxy(url) for url in proxy_urls if url.strip()]
            self._initialized = True
            
        except Exception as e:
            logger.error(f""Failed to load proxies: {str(e)}"")

    async def get_proxy(self) -> Optional[Proxy]:
        """"""Get next available proxy""""""
        if not self._initialized:
            await self.initialize()
            
        if not self.proxies:
            return None
            
        async with self._lock:
            # Filter out proxies with too many failures
            available_proxies = [p for p in self.proxies if p.fails < 3]
            
            if not available_proxies:
                # Reset failure counts if all proxies are failed
                for proxy in self.proxies:
                    proxy.fails = 0
                available_proxies = self.proxies
            
            return random.choice(available_proxies)

    async def mark_failed(self, proxy: Proxy):
        """"""Mark a proxy as failed""""""
        proxy.fails += 1
        logger.warning(f""Proxy {proxy.url} marked as failed ({proxy.fails} fails)"")