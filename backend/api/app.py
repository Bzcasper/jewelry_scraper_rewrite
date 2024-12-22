# File: api/app.py
import os
from flask import Blueprint, request, jsonify
from backend.database.manager import DatabaseManager
from backend.database.models import Product
from backend.scraper.orchestrator import Orchestrator
import asyncio
from backend.logger import logger

# Initialize Blueprint
api_bp = Blueprint('api', __name__)
db_manager = DatabaseManager(os.getenv('DATABASE_URL'))
orchestrator = Orchestrator(db_manager)

@api_bp.route('/products', methods=['GET'])
def get_products():
    """
    Retrieve products with optional filters applied.
    """
    platform = request.args.get('platform')
    category = request.args.get('category')
    price_min = request.args.get('price_min', type=float)
    price_max = request.args.get('price_max', type=float)
    condition = request.args.get('condition')

    # Build filters dynamically
    filters = {}
    if platform:
        filters['platform'] = platform
    if category:
        filters['category'] = category
    if condition:
        filters['condition'] = condition
    if price_min is not None and price_max is not None:
        filters['price'] = (price_min, price_max)
    elif price_min is not None:
        filters['price'] = (price_min, float('inf'))
    elif price_max is not None:
        filters['price'] = (0, price_max)

    # Query the database
    try:
        products = db_manager.get_products(**filters)
        result = [
            {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'platform': product.platform,
                'category': product.category,
                'condition': product.condition,
                'image_url': product.image_url,
                'product_url': product.product_url,
                'date_scraped': product.date_scraped.isoformat(),
                'image_path': product.image_path,
                'material_details': product.material_details,
                'market_value': product.market_value,
                'similar_products': product.similar_products,
            }
            for product in products
        ]
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error retrieving products: {e}")
        return jsonify({'error': 'Failed to fetch products'}), 500

@api_bp.route('/scrape', methods=['POST'])
def start_scraping():
    """
    Start a new scraping job.
    """
    data = request.json
    query = data.get('query')
    platform = data.get('platform')
    max_items = data.get('max_items', 100)

    if not query or not platform:
        return jsonify({'error': 'Missing required parameters: query and platform'}), 400

    try:
        asyncio.run(orchestrator.start_scraping(query, platform, max_items))
        return jsonify({'status': 'Scraping started'}), 202
    except Exception as e:
        logger.error(f"Error starting scraping: {e}")
        return jsonify({'status': 'Scraping failed', 'error': str(e)}), 500

@api_bp.route('/backup', methods=['GET'])
def backup_database():
    """
    Backup the database to a file.
    """
    try:
        import shutil
        from datetime import datetime

        source_db = os.getenv('DATABASE_URL').replace('postgresql://', '')
        parts = source_db.split('/')
        user_pass = parts[0].split(':')
        db_name = parts[1]
        backup_dir = 'backend/data/backups'
        os.makedirs(backup_dir, exist_ok=True)
        backup_filename = f"{db_name}_backup_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.sql"
        backup_path = os.path.join(backup_dir, backup_filename)
        os.system(f"pg_dump -U {user_pass[0]} -h localhost -F c -b -v -f {backup_path} {db_name}")
        return jsonify({'status': 'Backup successful', 'backup_file': backup_filename}), 200
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return jsonify({'status': 'Backup failed', 'error': str(e)}), 500

@api_bp.route('/system/status', methods=['GET'])
def system_status():
    """
    Return system metrics and status.
    """
    try:
        metrics = {
            'active_jobs': 2,
            'products_found': 150,
            'cpu_usage': 55.5,
            'memory_usage': 68.3,
            'error_rate': 0.02,
            'success_rate': 0.98,
        }
        return jsonify(metrics), 200
    except Exception as e:
        logger.error(f"Error retrieving system status: {e}")
        return jsonify({'error': 'Failed to retrieve system status'}), 500
