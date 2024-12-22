# backend/scraper/utils/cache_manager.py

import aioredis
import os

class CacheManager:
    def __init__(self):
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.create_redis_pool(os.getenv('CACHE_REDIS_URL', 'redis://redis:6379/0'))

    async def get(self, key):
        if not self.redis:
            await self.connect()
        return await self.redis.get(key, encoding='utf-8')

    async def set(self, key, value, expire=300):
        if not self.redis:
            await self.connect()
        await self.redis.set(key, value, expire=expire)

    async def close(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()
