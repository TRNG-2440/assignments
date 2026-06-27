import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.conn = psycopg.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )

    def cursor(self):
        return self.conn.cursor()
    
    def commit(self):
        self.conn.commit()
    
    def close(self):
        self.conn.close()