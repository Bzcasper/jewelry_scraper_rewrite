import os
from flask import Flask
from database.models import Base
from database.manager import DatabaseManager
from logger import logger

app = Flask(__name__)

# Set up database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://bobby:8040@localhost:5432/jewelry_scraper")
try:
    db_manager = DatabaseManager(DATABASE_URL)
    Base.metadata.create_all(db_manager.engine)
    logger.info("Database connected successfully.")
except Exception as e:
    logger.error(f"Failed to connect to database: {e}")
    raise

@app.route('/')
def home():
    return "API is running!"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
