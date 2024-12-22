# backend/app/utils/logger.py
import logging
import sys
from pathlib import Path
from ..config import settings

def get_logger(name: str) -> logging.Logger:
    """"""Configure and return a logger instance""""""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        Path(""logs"").mkdir(exist_ok=True)
        
        # File handler
        file_handler = logging.FileHandler(f""logs/{name}.log"")
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger