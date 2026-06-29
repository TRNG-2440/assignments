from dotenv import load_dotenv, dotenv_values

load_dotenv()

config = dotenv_values()

def conn_string():
    return (
        f"host={config["DB_HOST"]} "
        f"dbname={config["DB_NAME"]} "
        f"user={config["DB_USER"]} "
        f"password={config["DB_PASSWORD"]} "
        f"port={config["DB_PORT"]} "
        )