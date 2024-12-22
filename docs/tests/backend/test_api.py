import unittest
from backend.app import app
from unittest.mock import patch

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to Jewelry Scraper API', response.data)

    @patch('backend.api.app.orchestrator.start_scraping')
    def test_start_scraping(self, mock_start_scraping):
        mock_start_scraping.return_value = None
        response = self.app.post('/api/scrape', json={
            'query': 'gold ring',
            'platform': 'ebay',
            'max_items': 50
        })
        self.assertEqual(response.status_code, 202)
        self.assertIn(b'Scraping started', response.data)

    # Add more tests for API endpoints

if __name__ == '__main__':
    unittest.main()
