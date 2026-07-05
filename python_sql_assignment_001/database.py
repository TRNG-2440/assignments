import os
from pathlib import Path

import mysql.connector

# Declare host - localhost
HOST = os.getenv("MYSQL_HOST", "localhost")

# Declare user - root
USER = os.getenv("MYSQL_USER", "root")

# Declare password - whatever you decide
PASSWORD = os.getenv("MYSQL_PASSWORD", "")

# Declare database - library_db
DATABASE = os.getenv("MYSQL_DATABASE", "library_db")

# --------------------------------------------------------------------------------

# Produce connection to library database
def Connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE,
    )

# --------------------------------------------------------------------------------

# Create database connection
def Create_Database():

    # Establish interface between python app and database
    connection = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD)

    # Declare object that allows user to send queries
    cursor = connection.cursor()

    # Erase database if it currently exists
    cursor.execute(f"DROP DATABASE IF EXISTS {DATABASE}")

    # Create new database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")

    # Create database if it currently does not exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")

    # Save changes
    connection.commit()

    # End query tool
    cursor.close()

    # Close connection
    connection.close()

    # Produce tables through schema.sql
    schema = (Path(__file__).parent / "schema.sql").read_text(encoding="utf-8")

    # Instantiate connection
    connection = Connection()

    # Declare object that allows user to send queries
    cursor = connection.cursor()

    # Traverse through schema.sql and execute each command
    for scheme in schema.split(";"):
        if scheme.strip():
            cursor.execute(scheme)

    # Save changes
    connection.commit()

    # End query tool
    cursor.close()

    # Close connection
    connection.close()


# Assignment also refers to this as initialize_db()
initialize_db = Create_Database
