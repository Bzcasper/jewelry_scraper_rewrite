# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from app.core.config import Settings
from app.api.deps import get_db, get_current_user
from app.schemas import (
    JewelryCreate, 
    JewelryResponse, 
    ScrapingJob, 
    SystemMetrics,
    ExportFormat
)
from app.services import (
    jewelry_service,
    scraping_service,
    export_service,
    monitoring_service
)

settings = Settings()
app = FastAPI(title=""Jewelry Scraper API"")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=[""*""],
    allow_headers=[""*""],
)

# Scraping endpoints
@app.post(""/api/scrape"", response_model=ScrapingJob)
async def start_scraping(
    query: str,
    platform: str,
    max_items: int = 100,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """"""Start a new scraping job""""""
    return await scraping_service.start_scraping_job(
        query=query,
        platform=platform,
        max_items=max_items,
        background_tasks=background_tasks,
        user_id=current_user.id,
        db=db
    )

@app.get(""/api/scrape/{job_id}"", response_model=ScrapingJob)
async def get_scraping_status(
    job_id: str,
    current_user = Depends(get_current_user)
):
    """"""Get status of a scraping job""""""
    return await scraping_service.get_job_status(job_id)

# Product endpoints
@app.get(""/api/products"", response_model=List[JewelryResponse])
async def get_products(
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = None,
    platform: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """"""Get products with filtering and pagination""""""
    return await jewelry_service.get_products(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        platform=platform,
        min_price=min_price,
        max_price=max_price,
        condition=condition,
        sort_by=sort_by
    )

@app.get(""/api/products/export"")
async def export_products(
    format: ExportFormat,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """"""Export products in specified format""""""
    return await export_service.export_products(format, db)

# Monitoring endpoints
@app.get(""/api/system/metrics"", response_model=SystemMetrics)
async def get_system_metrics(
    current_user = Depends(get_current_user)
):
    """"""Get system metrics""""""
    return await monitoring_service.get_metrics()

@app.get(""/api/system/status"")
async def get_system_status():
    """"""Get system health status""""""
    return await monitoring_service.get_status()
# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
import logging
from datetime import datetime

from app.core.config import Settings
from app.api.deps import get_db, get_current_user
from app.schemas import (
    JewelryCreate, 
    JewelryResponse, 
    ScrapingJob, 
    SystemMetrics,
    ExportFormat
)
from app.services import (
    jewelry_service,
    scraping_service,
    export_service,
    monitoring_service
)

settings = Settings()
app = FastAPI(title=""Jewelry Scraper API"")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=[""*""],
    allow_headers=[""*""],
)

# Scraping endpoints
@app.post(""/api/scrape"", response_model=ScrapingJob)
async def start_scraping(
    query: str,
    platform: str,
    max_items: int = 100,
    background_tasks: BackgroundTasks,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """"""Start a new scraping job""""""
    return await scraping_service.start_scraping_job(
        query=query,
        platform=platform,
        max_items=max_items,
        background_tasks=background_tasks,
        user_id=current_user.id,
        db=db
    )

@app.get(""/api/scrape/{job_id}"", response_model=ScrapingJob)
async def get_scraping_status(
    job_id: str,
    current_user = Depends(get_current_user)
):
    """"""Get status of a scraping job""""""
    return await scraping_service.get_job_status(job_id)

# Product endpoints
@app.get(""/api/products"", response_model=List[JewelryResponse])
async def get_products(
    skip: int = 0,
    limit: int = 50,
    category: Optional[str] = None,
    platform: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    condition: Optional[str] = None,
    sort_by: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """"""Get products with filtering and pagination""""""
    return await jewelry_service.get_products(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        platform=platform,
        min_price=min_price,
        max_price=max_price,
        condition=condition,
        sort_by=sort_by
    )

@app.get(""/api/products/export"")
async def export_products(
    format: ExportFormat,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """"""Export products in specified format""""""
    return await export_service.export_products(format, db)

# Monitoring endpoints
@app.get(""/api/system/metrics"", response_model=SystemMetrics)
async def get_system_metrics(
    current_user = Depends(get_current_user)
):
    """"""Get system metrics""""""
    return await monitoring_service.get_metrics()

@app.get(""/api/system/status"")
async def get_system_status():
    """"""Get system health status""""""
    return await monitoring_service.get_status()