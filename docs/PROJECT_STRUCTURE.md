# Project Structure

Understanding the directory layout is crucial for navigating and contributing to the Jewelry Scraper project. Below is an overview of the project's structure.

\\\
jewelry_scraper/
│
├── backend/
│   ├── app.py
│   ├── Dockerfile
│   ├── logger.py
│   ├── scheduler.py
│   ├── scraper/
│   │   ├── spiders/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── ebay_spider.py
│   │   │   └── amazon_spider.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── proxy_manager.py
│   │   │   ├── rate_limiter.py
│   │   │   ├── user_agent_rotator.py
│   │   │   ├── image_processor.py
│   │   │   ├── product_validator.py
│   │   │   └── data_enricher.py
│   │   └── orchestrator.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── manager.py
│   │   └── models.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── app.py
│   └── config/
│       ├── __init__.py
│       ├── settings.py
│       ├── proxies.txt
│       ├── scraping.py
│       └── image_processing.py
│
├── frontend/
│   ├── Dockerfile
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── DataDashboard.js
│   │   │   ├── DataTable.js
│   │   │   ├── EnhancedSearch.js
│   │   │   ├── ProductCard.js
│   │   │   └── SystemMonitor.js
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── context/
│   │   │   └── AppContext.js
│   │   ├── App.js
│   │   ├── App.css
│   │   ├── index.js
│   │   └── index.css
│   ├── package.json
│   └── README.md
│
├── data/
│   ├── images/
│   └── backups/
│
├── logs/
│
├── tests/
│   ├── backend/
│   │   ├── test_spiders.py
│   │   ├── test_database.py
│   │   └── test_api.py
│   └── frontend/
│       └── components/
│           └── test_components.js
│
├── docs/
│   ├── CONFIGURATION.md
│   ├── USAGE.md
│   ├── PROJECT_STRUCTURE.md
│   ├── ADVANCED_FEATURES.md
│   ├── CLOUD_DEPLOYMENT_PLAN.md
│   └── ENHANCEMENT_ROADMAP.md
│
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── docker-compose.yml
├── prometheus.yml
├── LICENSE
├── README.md
└── CONTRIBUTING.md
\\\

Refer to each directory's README or respective documentation for more details.
