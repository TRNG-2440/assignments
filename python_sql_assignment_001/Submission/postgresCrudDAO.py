import psycopg

class genericDao:
    def __init__(self, conn_string:str):
        self.conn_string = conn_string
    
    def __get_connection(self):
        return psycopg.connect(self.conn_string)
    
    # DML
    def execute(self, query: str, params: tuple = ()):
        with self.__get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query= query, params= params)
                conn.commit()
                return cur.rowcount

    # DQL
    def get_one(self, query:str, params:tuple = ()):
        with self.__get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query= query, params= params)
                return cur.fetchone()

    def get_all(self, query:str, params:tuple = ()):
        with self.__get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query= query, params= params)
                return cur.fetchall()