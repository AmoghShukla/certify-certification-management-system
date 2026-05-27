import logging
import os

def get_logger(name : str):
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        if not os.path.exists('src/logs'):
            os.makedirs('src/logs', exist_ok=True)

        formatter = logging.Formatter(' %(asctime)s | %(levelname)s | %(name)s | %(message)s')
        
        consolehandler = logging.StreamHandler()
        consolehandler.setFormatter(formatter)
        logger.addHandler(consolehandler)

        filehandler = logging.FileHandler('src/logs/app.log')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

    return logger
