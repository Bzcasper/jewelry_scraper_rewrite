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
# app.py
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup
app = Flask(name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jewelry.db'
db = SQLAlchemy(app)

class Jewelry(db.Model):
id = db.Column(db.Integer, primary_key=True)
title = db.Column(db.String(100), nullable=False)
description = db.Column(db.Text, nullable=True)
price = db.Column(db.Float, nullable=False)
image_url = db.Column(db.String(200), nullable=True)
category = db.Column(db.String(50), nullable=True)

@app.route('/')
def index():
jewelry = Jewelry.query.all()
return render_template('index.html', jewelry=jewelry)

@app.route('/add_jewelry', methods=['POST'])
def add_jewelry():
data = request.json
new_jewelry = Jewelry(
title=data['title'],
description=data['description'],
price=data['price'],
image_url=data['image_url'],
category=data['category']
)
db.session.add(new_jewelry)
db.session.commit()
return jsonify({'message': 'Jewelry added successfully'}), 201

@app.route('/scrape', methods=['POST'])
def scrape_jewelry():
url = request.json['url']
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

title = soup.find('h1', {'class': 'product-title'}).text.strip()
description = soup.find('div', {'class': 'product-description'}).text.strip()
price = float(soup.find('span', {'class': 'price'}).text.strip().replace('$', ''))
image_url = soup.find('img', {'class': 'product-image'})['src']
category = soup.find('span', {'class': 'product-category'}).text.strip()

new_jewelry = Jewelry(
    title=title,
    description=description,
    price=price,
    image_url=image_url,
    category=category
)
db.session.add(new_jewelry)
db.session.commit()

return jsonify({'message': 'Jewelry scraped and added successfully'}), 201
@app.route('/search', methods=['GET'])
def search_jewelry():
query = request.args.get('q', '')
jewelry = Jewelry.query.filter(Jewelry.title.ilike(f'%{query}%')).all()
return jsonify([{
'id': item.id,
'title': item.title,
'description': item.description,
'price': item.price,
'image_url': item.image_url,
'category': item.category
} for item in jewelry])

if name == 'main':
db.create_all()
app.run(debug=True)