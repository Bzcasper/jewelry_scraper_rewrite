import os
from flask import Flask, jsonify
from flask_cors import CORS
from backend.app.db.models import Base
from database.manager import DatabaseManager
from logger import logger
from api.app import api_bp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes

# Set up database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bobby:8040@localhost:5432/jewelry_scraper")
try:
    db_manager = DatabaseManager(DATABASE_URL)
    Base.metadata.create_all(db_manager.engine)
    logger.info("Database connected successfully.")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    raise

# Register the API blueprint
app.register_blueprint(api_bp, url_prefix='/api')

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "database": "connected" if db_manager else "disconnected"
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.teardown_appcontext
def shutdown_session(exception=None):
    """Gracefully close database connections."""
    db_manager.close_session()

if __name__ == "__main__":
    # Set debug mode based on environment
    is_debug = os.getenv("FLASK_ENV", "development") == "development"
    app.run(debug=is_debug, host="0.0.0.0", port=5000)
# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_load
load_dotenv()

app = Flask(name)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///jewelry.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Jewelry(db.Model):
id = db.Column(db.Integer, primary_key=True)
title = db.Column(db.String(100), nullable=False)
description = db.Column(db.Text, nullable=True)
price = db.Column(db.Float, nullable=False)
image_url = db.Column(db.String(200), nullable=True)
category = db.Column(db.String(50), nullable=True)
brand = db.Column(db.String(50), nullable=True)
material = db.Column(db.String(50), nullable=True)
condition = db.Column(db.String(20), nullable=True)

@app.route('/')
def index():
jewelry = Jewelry.query.all()
return render_template('index.html', jewelry=jewelry)

@app.route('/api/jewelry', methods=['GET'])
def get_jewelry():
jewelry = Jewelry.query.all()
return jsonify([{
'id': item.id,
'title': item.title,
'description': item.description,
'price': item.price,
'image_url': item.image_url,
'category': item.category,
'brand': item.brand,
'material': item.material,
'condition': item.condition
} for item in jewelry])

@app.route('/api/jewelry', methods=['POST'])
def add_jewelry():
data = request.json
new_jewelry = Jewelry(
title=data['title'],
description=data.get('description'),
price=data['price'],
image_url=data.get('image_url'),
category=data.get('category'),
brand=data.get('brand'),
material=data.get('material'),
condition=data.get('condition')
)
db.session.add(new_jewelry)
db.session.commit()
return jsonify({'message': 'Jewelry added successfully', 'id': new_jewelry.id}), 201

@app.route('/api/scrape', methods=['POST'])
def scrape_jewelry():
url = request.json['url']
try:
response = requests.get(url, timeout=10)
soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1', {'itemprop': 'name'}).text.strip()
    price = float(soup.find('span', {'itemprop': 'price'}).text.strip().replace('$', '').replace(',', ''))
    description = soup.find('div', {'itemprop': 'description'}).text.strip()
    image_url = soup.find('img', {'itemprop': 'image'})['src']
    category = soup.find('span', {'itemprop': 'category'}).text.strip()
    brand = soup.find('span', {'itemprop': 'brand'}).text.strip()
    
    new_jewelry = Jewelry(
        title=title,
        description=description,
        price=price,
        image_url=image_url,
        category=category,
        brand=brand
    )
    db.session.add(new_jewelry)
    db.session.commit()
    
    return jsonify({'message': 'Jewelry scraped and added successfully', 'id': new_jewelry.id}), 201
except Exception as e:
    return jsonify({'error': str(e)}), 400
@app.route('/api/search', methods=['GET'])
def search_jewelry():
query = request.args.get('q', '')
category = request.args.get('category')
min_price = request.args.get('min_price', type=float)
max_price = request.args.get('max_price', type=float)

jewelry_query = Jewelry.query.filter(Jewelry.title.ilike(f'%{query}%'))

if category:
    jewelry_query = jewelry_query.filter(Jewelry.category == category)
if min_price:
    jewelry_query = jewelry_query.filter(Jewelry.price >= min_price)
if max_price:
    jewelry_query = jewelry_query.filter(Jewelry.price <= max_price)

jewelry = jewelry_query.all()
return jsonify([{
    'id': item.id,
    'title': item.title,
    'description': item.description,
    'price': item.price,
    'image_url': item.image_url,
    'category': item.category,
    'brand': item.brand,
    'material': item.material,
    'condition': item.condition
} for item in jewelry])
if name == 'main':
db.create_all()
app.run(debug=True)