from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
import logging
import asyncio
import uuid
from datetime import datetime
from database.manager import DatabaseManager
from orchestrator import ScrapingOrchestrator

app = FastAPI(title="Enhanced Jewelry Scraper API", version="1.1.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
db = DatabaseManager()
orchestrator = ScrapingOrchestrator()

# Define models
class ScrapeRequest(BaseModel):
    query: str
    platform: str = Field(default="ebay", regex="^(ebay|amazon)$")
    max_items: int = Field(default=50, ge=1, le=200)
    filters: Optional[Dict] = {}

class Product(BaseModel):
    id: int
    title: str
    price: float
    currency: str
    url: str
    platform: str
    description: Optional[str]
    images: List[str]
    category: Optional[str]
    brand: Optional[str]
    specifications: Dict
    external_id: Optional[str]
    date_scraped: datetime

class JobStatus(BaseModel):
    id: str
    status: str
    progress: float
    items_scraped: int
    error: Optional[str]
    start_time: datetime

# API endpoints
@app.post("/scrape", response_model=Dict)
async def start_scraping(request: ScrapeRequest, background_tasks: BackgroundTasks):
    """Start a new scraping job"""
    job_id = await orchestrator.start_scraping(str(uuid.uuid4()), request.dict())
    if not job_id:
        raise HTTPException(status_code=500, detail="Failed to start scraping job.")
    return {"job_id": job_id}

@app.get("/scrape/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str):
    """Get the status of a scraping job"""
    status = await orchestrator.get_task_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return status

@app.get("/products", response_model=Dict)
async def get_products(
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=100),
    platform: Optional[str] = None,
    category: Optional[str] = None,
    price_min: Optional[float] = None,
    price_max: Optional[float] = None,
    search: Optional[str] = None,
    sort_by: str = Query("date_scraped"),
    sort_desc: bool = True
):
    """Get products with pagination and filters"""
    filters = {k: v for k, v in locals().items() if k not in ("page", "per_page", "sort_by", "sort_desc") and v is not None}
    products, total = await db.get_products(filters, page, per_page, sort_by, sort_desc)
    return {
        "products": products,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

@app.get("/system/status", response_model=Dict)
async def get_system_status():
    """Get system metrics and job statistics"""
    stats = orchestrator.get_summary()
    return stats

# Cleanup hooks
@app.on_event("shutdown")
async def shutdown():
    await orchestrator.cleanup()

# Database Manager
class DatabaseManager:
    def __init__(self):
        # Initialization logic for database connections
        pass

    async def get_products(self, filters, page, per_page, sort_by, sort_desc):
        """Fetch products from the database."""
        # Logic for fetching products with pagination and filters
        return [], 0

# Scraping Orchestrator
class ScrapingOrchestrator:
    def __init__(self):
        self.active_jobs = {}

    async def start_scraping(self, task_id, params):
        """Start a new scraping job."""
        # Logic to start scraping job
        self.active_jobs[task_id] = {
            "status": "running",
            "progress": 0.0,
            "items_scraped": 0,
            "start_time": datetime.now()
        }
        return task_id

    async def get_task_status(self, task_id):
        """Get the status of a scraping job."""
        return self.active_jobs.get(task_id)

    def get_summary(self):
        """Return system metrics and summary of scraping jobs."""
        return {
            "active_jobs": len(self.active_jobs),
            "total_jobs": len(self.active_jobs)
        }

    async def cleanup(self):
        """Cleanup logic for resources."""
        self.active_jobs.clear()
