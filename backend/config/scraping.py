# config/scraping.py

SCRAPING_CONFIG = {
    'ebay': {
        'max_items_per_search': 100,
        'search_delay': 2.0,
        'retry_attempts': 3,
        'categories': [
            'Rings',
            'Necklaces',
            'Bracelets',
            'Earrings'
        ]
    },
    'amazon': {
        'max_items_per_search': 100,
        'search_delay': 2.5,
        'retry_attempts': 3,
        'categories': [
            'Jewelry',
            'Fine Jewelry',
            'Fashion Jewelry'
        ]
    }
}
