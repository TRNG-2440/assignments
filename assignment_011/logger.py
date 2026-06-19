import logging
import sys

# Get the root logger
logger = logging.getLogger()

# Clean up existing handlers to avoid duplicate logs (e.g., from Uvicorn defaults)
if logger.hasHandlers():
    logger.handlers.clear()

# Set global logging level
logger.setLevel(logging.INFO)

# Define custom log format
log_format = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# StreamHandler outputs to the console (stdout)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)
