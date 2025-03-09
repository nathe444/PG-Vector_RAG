import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DBNAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}

def create_database():
    """Creates the 'rag_db' database if it doesn't exist."""
    # Connect to the default PostgreSQL database
    default_config = DB_CONFIG.copy()
    default_config['dbname'] = 'postgres'
    
    try:
        conn = psycopg2.connect(**default_config)
        conn.set_session(autocommit=True)  # Ensure autocommit mode for CREATE DATABASE
        cur = conn.cursor()

        # Check if rag_db exists
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'rag_db'")
        if not cur.fetchone():
            print("Database 'rag_db' does not exist. Creating it...")
            cur.execute("CREATE DATABASE rag_db")
            print("Database 'rag_db' created successfully.")

        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        raise

def create_tables():
    """Creates the necessary database tables."""
    DB_CONFIG['dbname'] = 'rag_db'  # Switch to the 'rag_db' database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS document_metadata (
            document_id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            source VARCHAR(255),
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunk (
            chunk_id SERIAL PRIMARY KEY,
            document_id INT REFERENCES document_metadata(document_id),
            chunk_number INT,
            chunk_text TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS embedding (
            chunk_id INT REFERENCES chunk(chunk_id),
            embedding_vector FLOAT8[]
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS document_vectors (
            id SERIAL PRIMARY KEY,
            chunk_id INT REFERENCES chunk(chunk_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def document_exists_in_db(document_path):
    """Checks if the document exists in the database."""
    DB_CONFIG['dbname'] = 'rag_db'  # Switch to the 'rag_db' database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT document_id FROM document_metadata WHERE title = %s", (document_path,))
    document_id = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    return document_id is not None

def main():
    create_database()  # Ensure the database exists before creating tables
    create_tables()    # Create the tables in the database

if __name__ == "__main__":
    main()
