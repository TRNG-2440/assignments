"""
Logging configuration for app
"""
import logging

# logger
logging.basicConfig(
    level = logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# create logger in main module
logger = logging.getLogger(__name__)