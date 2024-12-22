import unittest
from unittest.mock import MagicMock, patch
from backend.scraper.orchestrator import Orchestrator
from backend.database.manager import DatabaseManager

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        self.db_manager = MagicMock(spec=DatabaseManager)
        self.orchestrator = Orchestrator(self.db_manager)
    
    @patch('backend.scraper.orchestrator.EbaySpider')
    @patch('backend.scraper.orchestrator.CrawlerProcess')
    def test_start_scraping_ebay(self, mock_crawler_process, mock_ebay_spider):
        query = 'silver necklace'
        platform = 'ebay'
        max_items = 50

        self.orchestrator.start_scraping(query, platform, max_items)

        mock_ebay_spider.assert_called_with(query=query, max_items=max_items)
        mock_crawler_process.return_value.crawl.assert_called_once_with(mock_ebay_spider.return_value)
        mock_crawler_process.return_value.start.assert_called_once()

    # Add more tests for Orchestrator

if __name__ == '__main__':
    unittest.main()
