import scrapy
from backend.scraper.spiders.base import BaseSpider
from backend.database.manager import DatabaseManager
from backend.database.models import Product
from datetime import datetime

class AmazonSpider(BaseSpider):
    name = 'amazon'

    def start_requests(self):
        query = getattr(self, 'query', 'gold ring')
        max_items = int(getattr(self, 'max_items', 100))
        search_url = f'https://www.amazon.com/s?k={query}'
        yield self.make_request(url=search_url, callback=self.parse, meta={'max_items': max_items})

    def parse(self, response):
        max_items = response.meta.get('max_items', 100)
        products = response.css('.s-result-item')

        for product in products:
            if max_items <= 0:
                return

            name = product.css('h2 a span::text').get()
            price_whole = product.css('.a-price-whole::text').get()
            price_fraction = product.css('.a-price-fraction::text').get()
            price = self.extract_price(price_whole, price_fraction)
            platform = 'Amazon'
            category = 'Rings'  # Simplified for example
            condition = product.css('.a-color-secondary::text').get()
            image_url = product.css('.s-image::attr(src)').get()
            product_url = product.css('h2 a::attr(href)').get()

            yield {
                'name': name,
                'price': price,
                'platform': platform,
                'category': category,
                'condition': condition,
                'image_url': image_url,
                'product_url': f'https://www.amazon.com{product_url}' if product_url else '',
                'date_scraped': datetime.utcnow()
            }

            max_items -= 1

        # Pagination logic
        next_page = response.css('li.a-last a::attr(href)').get()
        if next_page and max_items > 0:
            yield self.make_request(url=f'https://www.amazon.com{next_page}', callback=self.parse, meta={'max_items': max_items})

    def extract_price(self, whole, fraction):
        try:
            return float(f"{whole}{fraction}")
        except:
            return 0.0
