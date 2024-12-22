# backend/app/db/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = ""users""
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    products = relationship(""Product"", back_populates=""owner"")

class Product(Base):
    __tablename__ = ""products""
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    price = Column(Float, index=True)
    currency = Column(String, default=""USD"")
    category = Column(String, index=True)
    platform = Column(String, index=True)
    url = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey(""users.id""))
    owner = relationship(""User"", back_populates=""products"")

class ScrapingJob(Base):
    __tablename__ = ""scraping_jobs""
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String)
    platform = Column(String)
    status = Column(String)  # pending, running, completed, failed
    items_found = Column(Integer, default=0)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    error = Column(Text)
    owner_id = Column(Integer, ForeignKey(""users.id""))
    owner = relationship(""User"")