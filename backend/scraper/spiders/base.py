import scrapy
from backend.scraper.utils.proxy_manager import ProxyManager
from backend.scraper.utils.rate_limiter import RateLimiter
from backend.scraper.utils.user_agent_rotator import UserAgentRotator

class BaseSpider(scrapy.Spider):
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 8,
        'RETRY_TIMES': 3,
        'ROBOTSTXT_OBEY': False,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...'
    }

    def __init__(self, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.proxy_manager = ProxyManager()
        self.rate_limiter = RateLimiter(max_requests=60, time_window=60)
        self.user_agent_rotator = UserAgentRotator()

    def start_requests(self):
        raise NotImplementedError("Define start_requests method")

    def parse(self, response):
        raise NotImplementedError("Define parse method")

    def make_request(self, url, callback):
        proxy = self.proxy_manager.get_proxy()
        user_agent = self.user_agent_rotator.get_user_agent()
        return scrapy.Request(
            url=url,
            callback=callback,
            meta={'proxy': proxy},
            headers={'User-Agent': user_agent}
        )
