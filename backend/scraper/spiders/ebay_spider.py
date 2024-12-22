import scrapy
from backend.scraper.spiders.base import BaseSpider
from backend.database.manager import DatabaseManager
from backend.database.models import Product
from datetime import datetime

class EbaySpider(BaseSpider):
    name = 'ebay'

    def start_requests(self):
        query = getattr(self, 'query', 'gold ring')
        max_items = int(getattr(self, 'max_items', 100))
        search_url = f'https://www.ebay.com/sch/i.html?_nkw={query}'
        yield self.make_request(url=search_url, callback=self.parse, meta={'max_items': max_items})

    def parse(self, response):
        max_items = response.meta.get('max_items', 100)
        products = response.css('.s-item')

        for product in products:
            if max_items <= 0:
                return

            name = product.css('.s-item__title::text').get()
            price_text = product.css('.s-item__price::text').get()
            price = self.extract_price(price_text)
            platform = 'eBay'
            category = 'Rings'  # Simplified for example
            condition = product.css('.SECONDARY_INFO::text').get()
            image_url = product.css('.s-item__image-img::attr(src)').get()
            product_url = product.css('.s-item__link::attr(href)').get()

            yield {
                'name': name,
                'price': price,
                'platform': platform,
                'category': category,
                'condition': condition,
                'image_url': image_url,
                'product_url': product_url,
                'date_scraped': datetime.utcnow()
            }

            max_items -= 1

        # Pagination logic
        next_page = response.css('.pagination__next::attr(href)').get()
        if next_page and max_items > 0:
            yield self.make_request(url=next_page, callback=self.parse, meta={'max_items': max_items})

    def extract_price(self, price_text):
        try:
            return float(price_text.replace('$','').replace(',','').split(' ')[0])
        except:
            return 0.0
