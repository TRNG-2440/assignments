import os
from dotenv import load_dotenv

load_dotenv()

def get_conn_string() -> str:
    return (
        f"host={os.environ.get('DB_HOST')} "
        f"dbname={os.environ.get('DB_NAME')} "
        f"user={os.environ.get('DB_USER')} "
        f"password={os.environ.get('DB_PASSWORD')} "
        f"port={os.environ.get('DB_PORT')}"
    )