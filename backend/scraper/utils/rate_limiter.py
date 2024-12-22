import asyncio
import time

class RateLimiter:
    def __init__(self, max_requests, time_window):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []

    async def allow_request(self):
        current_time = time.time()
        self.requests = [req for req in self.requests if req > current_time - self.time_window]
        if len(self.requests) < self.max_requests:
            self.requests.append(current_time)
            return True
        return False
