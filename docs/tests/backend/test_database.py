import unittest
from backend.database.manager import DatabaseManager
from backend.app.db.models import Base, Product

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager('sqlite:///:memory:')
        Base.metadata.create_all(self.db_manager.engine)

    def test_add_product(self):
        product_data = {
            'name': 'Test Ring',
            'price': 99.99,
            'platform': 'eBay',
            'category': 'Rings',
            'condition': 'New',
            'image_url': 'http://example.com/image.jpg',
            'product_url': 'http://example.com/product',
            'date_scraped': '2023-01-01T00:00:00'
        }
        self.db_manager.add_product(product_data)
        products = self.db_manager.get_products(platform='eBay')
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, 'Test Ring')

    # Add more tests for DatabaseManager

if __name__ == '__main__':
    unittest.main()
