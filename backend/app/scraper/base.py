# backend/app/scrapers/base.py
from abc import ABC, abstractmethod
from typing import List, Dict
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from app.core.config import settings
from app.utils.proxy import ProxyManager
from app.utils.rate_limiter import RateLimiter

class BaseScraper(ABC):
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.rate_limiter = RateLimiter()
        self.session = None
    
    async def init_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def close_session(self):
        if self.session:
            await self.session.close()
            self.session = None
    
    @abstractmethod
    async def search_products(self, query: str, max_items: int) -> List[Dict]:
        pass
    
    async def get_page(self, url: str) -> str:
        await self.rate_limiter.wait()
        proxy = await self.proxy_manager.get_proxy()
        
        try:
            async with self.session.get(url, proxy=proxy) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    raise Exception(f""Failed to fetch page: {response.status}"")
        except Exception as e:
            await self.proxy_manager.mark_proxy_failed(proxy)
            raise