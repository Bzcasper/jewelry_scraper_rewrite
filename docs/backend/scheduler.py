from apscheduler.schedulers.background import BackgroundScheduler
from backend.database.manager import DatabaseManager
from backend.app.db.models import Product
import os
import logging


def backup_database():
    try:
        db_url = os.getenv('DATABASE_URL')
        db_manager = DatabaseManager(db_url)
        # Implement backup logic, e.g., dump the database
        import shutil
        from datetime import datetime

        source_db = db_url.replace('postgresql://', '')
        parts = source_db.split('/')
        user_pass = parts[0].split(':')
        db_name = parts[1]
        backup_dir = 'backend/data/backups'
        os.makedirs(backup_dir, exist_ok=True)
        backup_filename = f"{db_name}_backup_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.sql"
        backup_path = os.path.join(backup_dir, backup_filename)
        os.system(f"pg_dump -U {user_pass[0]} -h db -F c -b -v -f {backup_path} {db_name}")
        logger.info(f"Database backup completed: {backup_filename}")
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        send_error_notification(str(e))

scheduler = BackgroundScheduler()
scheduler.add_job(backup_database, 'interval', hours=24)
