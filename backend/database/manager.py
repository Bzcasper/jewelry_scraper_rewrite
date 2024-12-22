from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.logger import logger

class DatabaseManager:
    def __init__(self, database_url):
        try:
            self.engine = create_engine(database_url)
            self.Session = sessionmaker(bind=self.engine)
            logger.info("Database connection established.")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def get_products(self, **filters):
        session = self.Session()
        try:
            # Example filter implementation
            query = session.query(Product)
            for key, value in filters.items():
                if key == 'price':
                    query = query.filter(Product.price.between(*value))
                else:
                    query = query.filter(getattr(Product, key) == value)
            return query.all()
        finally:
            session.close()
