import asyncio
from typing import Dict, Optional
import logging
from collections import defaultdict, deque
from datetime import datetime, timedelta

class AdaptiveRateLimiter:
    """An adaptive rate limiter that adjusts based on success and failure rates"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.rate_limits: Dict[str, float] = defaultdict(lambda: 1.0)  # Default to 1 request per second
        self.history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))  # Track the last 100 requests
        self.success_rate: Dict[str, float] = defaultdict(lambda: 1.0)  # Default success rate is 100%

    async def wait(self, platform: str):
        """Wait for the appropriate amount of time based on the platform's rate limit"""
        now = datetime.now()
        
        if platform not in self.history:
            self.history[platform].append(now)
            return

        last_request = self.history[platform][-1]
        elapsed = (now - last_request).total_seconds()

        # Calculate sleep time based on rate limit
        sleep_time = max(0, (1 / self.rate_limits[platform]) - elapsed)
        if sleep_time > 0:
            self.logger.info(f"Rate limiting {platform}: sleeping for {sleep_time:.2f}s")
            await asyncio.sleep(sleep_time)

        # Record this request
        self.history[platform].append(datetime.now())

    def update_success_rate(self, success: bool, platform: str):
        """Update the success rate of requests for a platform"""
        if platform not in self.history:
            self.logger.warning(f"Platform {platform} not initialized in rate limiter.")
            return

        # Adjust success rate based on outcome
        self.success_rate[platform] = (
            min(1.0, self.success_rate[platform] + 0.01) if success else max(0.0, self.success_rate[platform] - 0.05)
        )

        # Adjust rate limit based on success rate
        self.rate_limits[platform] = max(0.1, self.success_rate[platform])

        self.logger.info(
            f"Updated success rate for {platform}: {self.success_rate[platform]:.2f}, rate limit: {self.rate_limits[platform]:.2f} req/s"
        )

    def get_rate_limit(self, platform: str) -> float:
        """Get the current rate limit for a platform"""
        return self.rate_limits.get(platform, 1.0)

    def get_success_rate(self, platform: str) -> float:
        """Get the current success rate for a platform"""
        return self.success_rate.get(platform, 1.0)
# backend/app/utils/rate_limiter.py
import asyncio
import time
from ..config import settings

class RateLimiter:
    """"""Rate limiter for controlling request frequency""""""
    
    def __init__(self, requests_per_second: float = None):
        self.requests_per_second = requests_per_second or (1 / settings.REQUEST_DELAY)
        self.last_request = 0
        self._lock = asyncio.Lock()

    async def wait(self):
        """"""Wait for the appropriate delay between requests""""""
        async with self._lock:
            now = time.time()
            time_since_last = now - self.last_request
            delay_needed = (1 / self.requests_per_second) - time_since_last
            
            if delay_needed > 0:
                await asyncio.sleep(delay_needed)
            
            self.last_request = time.time()