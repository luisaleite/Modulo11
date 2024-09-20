# src/connectors/supabase_connector.py
import logging
import psycopg2
import pandas as pd
import sys
import os

# Add the top-level 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import configuration values from config.py
from src.config.config import SUPABASE_DB, SUPABASE_USER, SUPABASE_PASSWORD, SUPABASE_HOST, SUPABASE_PORT, TIMEOUT

def connect_to_supabase():
    """Connect to Supabase PostgreSQL."""
    logging.info("Connecting to Supabase PostgreSQL...")
    try:
        conn = psycopg2.connect(
            dbname=SUPABASE_DB,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            options=f"-c statement_timeout={TIMEOUT}"
        )
        logging.info("Connection to Supabase established.")
        return conn
    except psycopg2.Error as e:
        logging.error(f"Error connecting to Supabase: {e}")
        raise

def fetch_supabase_metrics():
    """Fetch telemetry data from Supabase database."""
    conn = connect_to_supabase()
    query = """
    SELECT 
        schemaname,
        relname AS table_name,
        n_live_tup AS row_count,
        pg_size_pretty(pg_total_relation_size(relid)) AS total_size
    FROM 
        pg_stat_user_tables;
    """
    try:
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        logging.error(f"Error fetching telemetry data from Supabase: {e}")
        conn.close()
        raise