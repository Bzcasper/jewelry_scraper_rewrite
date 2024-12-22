# scraper/jewelry_spider.py

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy.exceptions import DropItem
from jewelry_scraper.items import JewelryItem
import re

class JewelrySpider(scrapy.Spider):
name = 'jewelry'
allowed_domains = ['example-jewelry-site.com']
start_urls = ['https://www.example-jewelry-site.com/jewelry']

custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'ROBOTSTXT_OBEY': True,
    'CONCURRENT_REQUESTS': 16,
    'DOWNLOAD_DELAY': 1,
    'COOKIES_ENABLED': False,
}

def parse(self, response):
    for product in response.css('div.product-item'):
        loader = ItemLoader(item=JewelryItem(), selector=product)
        loader.default_output_processor = TakeFirst()

        loader.add_css('title', 'h2.product-title::text')
        loader.add_css('price', 'span.price::text', MapCompose(self.parse_price))
        loader.add_css('image_url', 'img.product-image::attr(src)')
        loader.add_css('category', 'span.category::text')
        loader.add_css('brand', 'span.brand::text')
        loader.add_css('material', 'span.material::text')
        loader.add_xpath('description', '//div[@class=""product-description""]//text()', Join())
        
        yield loader.load_item()

    next_page = response.css('a.next-page::attr(href)').get()
    if next_page:
        yield response.follow(next_page, self.parse)

def parse_price(self, value):
    try:
        return float(re.sub(r'[^\d.]', '', value))
    except ValueError:
        raise DropItem(""Invalid price format"")

def parse_item(self, response):
    loader = ItemLoader(item=JewelryItem(), response=response)
    loader.default_output_processor = TakeFirst()

    loader.add_xpath('title', '//h1[@class=""product-title""]/text()')
    loader.add_xpath('price', '//span[@class=""price""]/text()', MapCompose(self.parse_price))
    loader.add_xpath('image_url', '//img[@id=""main-product-image""]/@src')
    loader.add_xpath('category', '//span[@class=""product-category""]/text()')
    loader.add_xpath('brand', '//span[@class=""product-brand""]/text()')
    loader.add_xpath('material', '//span[@class=""product-material""]/text()')
    loader.add_xpath('description', '//div[@class=""product-description""]//text()', Join())
    
    yield loader.load_item()

def errback_httpbin(self, failure):
    self.logger.error(repr(failure))

    if failure.check(HttpError):
        response = failure.value.response
        self.logger.error(f'HttpError on {response.url}')
    elif failure.check(DNSLookupError):
        request = failure.request
        self.logger.error(f'DNSLookupError on {request.url}')
    elif failure.check(TimeoutError, TCPTimedOutError):
        request = failure.request
        self.logger.error(f'TimeoutError on {request.url}')