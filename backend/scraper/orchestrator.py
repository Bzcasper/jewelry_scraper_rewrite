import asyncio
from backend.scraper.spiders.ebay_spider import EbaySpider
from backend.scraper.spiders.amazon_spider import AmazonSpider
from backend.database.manager import DatabaseManager
from backend.scraper.utils.image_processor import ImageProcessor
from backend.scraper.utils.product_validator import ProductValidator
from backend.scraper.utils.data_enricher import DataEnricher
from backend.logger import logger

class Orchestrator:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.image_processor = ImageProcessor()
        self.validator = ProductValidator()
        self.enricher = DataEnricher()

    async def start_scraping(self, query, platform, max_items):
        if platform.lower() == 'ebay':
            spider = EbaySpider(query=query, max_items=max_items)
        elif platform.lower() == 'amazon':
            spider = AmazonSpider(query=query, max_items=max_items)
        else:
            raise ValueError("Unsupported platform")

        # Integrate Scrapy's CrawlerProcess to run the spider
        from scrapy.crawler import CrawlerProcess
        from scrapy.utils.project import get_project_settings

        process = CrawlerProcess(settings=get_project_settings())
        process.crawl(spider)
        process.start()  # the script will block here until the crawling is finished

        # After scraping, process products
        products = self.db_manager.get_products(platform=platform)
        await self.process_products(products)

    async def process_products(self, products):
        tasks = []
        for product in products:
            if self.validator.validate(product):
                enriched_product = await self.enricher.enrich_product(product)
                image_path = await self.image_processor.process_image(product.image_url)
                enriched_product['image_path'] = image_path
                self.db_manager.update_product(enriched_product)
                tasks.append(enriched_product)
            else:
                logger.error(f"Validation failed for product: {product.name}")

        await asyncio.gather(*tasks)
