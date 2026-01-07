import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_dir: str = "logs") -> logging.Logger:
    """Setup logging configuration."""
    Path(log_dir).mkdir(exist_ok=True)
    
    log_file = Path(log_dir) / f"encryptor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {log_file}")
    return logger

def get_logger() -> logging.Logger:
    """Get logger instance."""
    return logging.getLogger(__name__)
