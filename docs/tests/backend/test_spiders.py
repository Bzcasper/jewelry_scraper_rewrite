import unittest
from backend.scraper.spiders.ebay_spider import EbaySpider
from backend.scraper.spiders.amazon_spider import AmazonSpider

class TestEbaySpider(unittest.TestCase):
    def setUp(self):
        self.spider = EbaySpider(query='gold ring', max_items=10)

    def test_spider_name(self):
        self.assertEqual(self.spider.name, 'ebay')

    # Add more tests for EbaySpider

class TestAmazonSpider(unittest.TestCase):
    def setUp(self):
        self.spider = AmazonSpider(query='gold ring', max_items=10)

    def test_spider_name(self):
        self.assertEqual(self.spider.name, 'amazon')

    # Add more tests for AmazonSpider

if __name__ == '__main__':
    unittest.main()
