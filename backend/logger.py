import os
import logging

# Resolve paths dynamically
base_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(base_dir, "logs")

# Ensure logs directory exists
os.makedirs(log_dir, exist_ok=True)

# Configure logger
log_file = os.path.join(log_dir, "app.log")
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

# Add FileHandler
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
