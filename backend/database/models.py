from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    platform = Column(String, nullable=False)
    category = Column(String, nullable=False)
    condition = Column(String)
    image_url = Column(String)
    product_url = Column(String)
    date_scraped = Column(DateTime)
    image_path = Column(String)  # Path to processed image
    material_details = Column(String)  # JSON string
    market_value = Column(Float)
    similar_products = Column(String)  # JSON string
