# backend/app/services/scraping.py
from typing import List, Dict, Optional, Any
import asyncio
import uuid
from datetime import datetime
from fastapi import BackgroundTasks
from ..models.product import Product
from ..models.scraping_job import ScrapingJob
from ..database import get_db
from ..scraper.spiders import EbaySpider, AmazonSpider
from ..utils.logger import get_logger
from ..cache import redis_client
from ..config import settings

logger = get_logger(__name__)

class ScrapingService:
    """"""Service for managing scraping operations""""""
    
    SPIDERS = {
        'ebay': EbaySpider,
        'amazon': AmazonSpider
    }

    def __init__(self):
        self.active_jobs: Dict[str, Dict] = {}
        self.redis = redis_client

    @classmethod
    async def start_job(
        cls,
        query: str,
        platform: str,
        max_items: int,
        background_tasks: BackgroundTasks,
        user_id: int
    ) -> str:
        """"""Start a new scraping job""""""
        job_id = str(uuid.uuid4())
        
        # Create job record
        job = ScrapingJob(
            id=job_id,
            user_id=user_id,
            query=query,
            platform=platform,
            max_items=max_items,
            status=""pending"",
            created_at=datetime.utcnow()
        )
        
        db = next(get_db())
        db.add(job)
        db.commit()

        # Add job to background tasks
        background_tasks.add_task(
            cls._run_scraping_job,
            job_id=job_id,
            query=query,
            platform=platform,
            max_items=max_items
        )

        return job_id

    @classmethod
    async def _run_scraping_job(
        cls,
        job_id: str,
        query: str,
        platform: str,
        max_items: int
    ):
        """"""Execute the scraping job""""""
        logger.info(f""Starting scraping job {job_id} for {platform}"")
        
        try:
            # Update job status
            await cls._update_job_status(job_id, ""running"")
            
            # Initialize spider
            spider_class = cls.SPIDERS.get(platform)
            if not spider_class:
                raise ValueError(f""Unsupported platform: {platform}"")
            
            spider = spider_class()
            
            # Perform scraping
            products = await spider.search_products(query, max_items)
            
            # Process and store products
            await cls._process_products(products, job_id)
            
            # Update job status
            await cls._update_job_status(
                job_id,
                ""completed"",
                metadata={""total_products"": len(products)}
            )
            
            logger.info(f""Completed scraping job {job_id}"")
            
        except Exception as e:
            logger.error(f""Error in scraping job {job_id}: {str(e)}"")
            await cls._update_job_status(
                job_id,
                ""failed"",
                metadata={""error"": str(e)}
            )

    @staticmethod
    async def _process_products(products: List[Dict], job_id: str):
        """"""Process and store scraped products""""""
        db = next(get_db())
        
        for product_data in products:
            try:
                # Check if product already exists
                existing_product = db.query(Product).filter(
                    Product.product_url == product_data['product_url']
                ).first()
                
                if existing_product:
                    # Update existing product
                    for key, value in product_data.items():
                        setattr(existing_product, key, value)
                    existing_product.updated_at = datetime.utcnow()
                else:
                    # Create new product
                    product = Product(**product_data)
                    db.add(product)
                
                db.commit()
                
            except Exception as e:
                logger.error(f""Error processing product in job {job_id}: {str(e)}"")
                db.rollback()

    @staticmethod
    async def _update_job_status(
        job_id: str,
        status: str,
        metadata: Optional[Dict] = None
    ):
        """"""Update job status in database""""""
        db = next(get_db())
        try:
            job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
            if job:
                job.status = status
                job.metadata = metadata or {}
                job.updated_at = datetime.utcnow()
                db.commit()
        except Exception as e:
            logger.error(f""Error updating job status: {str(e)}"")
            db.rollback()

    @staticmethod
    async def get_job_status(job_id: str) -> Optional[Dict]:
        """"""Get status of a scraping job""""""
        db = next(get_db())
        job = db.query(ScrapingJob).filter(ScrapingJob.id == job_id).first()
        
        if not job:
            return None
            
        return {
            ""job_id"": job.id,
            ""status"": job.status,
            ""created_at"": job.created_at,
            ""updated_at"": job.updated_at,
            ""metadata"": job.metadata
        }

    @staticmethod
    async def get_products(
        skip: int = 0,
        limit: int = 50,
        platform: Optional[str] = None,
        category: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        search: Optional[str] = None
    ) -> List[Dict]:
        """"""Get scraped products with filtering""""""
        db = next(get_db())
        query = db.query(Product)
        
        # Apply filters
        if platform:
            query = query.filter(Product.platform == platform)
        if category:
            query = query.filter(Product.category == category)
        if min_price is not None:
            query = query.filter(Product.price >= min_price)
        if max_price is not None:
            query = query.filter(Product.price <= max_price)
        if search:
            search_term = f""%{search}%""
            query = query.filter(Product.title.ilike(search_term))
        
        # Apply pagination
        query = query.offset(skip).limit(limit)
        
        # Execute query
        products = query.all()
        
        return [product.to_dict() for product in products]

    @staticmethod
    async def cleanup_old_jobs(days: int = 7):
        """"""Clean up old scraping jobs""""""
        db = next(get_db())
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        try:
            db.query(ScrapingJob).filter(
                ScrapingJob.created_at < cutoff_date,
                ScrapingJob.status.in_(['completed', 'failed'])
            ).delete()
            
            db.commit()
        except Exception as e:
            logger.error(f""Error cleaning up old jobs: {str(e)}"")
            db.rollback()