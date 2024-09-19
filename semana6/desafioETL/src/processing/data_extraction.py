import psycopg2
import pandas as pd
import logging
from tqdm import tqdm
import os

BATCH_SIZE = int(os.getenv("BATCH_SIZE", 15000))  # Dynamically set batch size

def list_supabase_tables(conn):
    """Lists the tables in Supabase."""
    logging.info("Listing tables in Supabase...")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'private_schema'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        logging.info(f"Found tables in Supabase: {table_names}")
        return table_names
    except psycopg2.Error as e:
        logging.error(f"Error listing tables in Supabase: {e}")
        raise


def extract_data_from_supabase(conn, table_name):
    """Extracts data from the specified Supabase table."""
    logging.info(f"Extracting data from table '{table_name}' in Supabase...")
    cursor = conn.cursor()
    query = f"SELECT * FROM private_schema.{table_name}"
    try:
        cursor.execute(query)
        while True:
            rows = cursor.fetchmany(BATCH_SIZE)
            if not rows:
                break
            yield pd.DataFrame(rows, columns=[desc[0] for desc in cursor.description])
    except psycopg2.Error as e:
        logging.error(f"Error extracting data from '{table_name}' in Supabase: {e}")
        raise