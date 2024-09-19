import logging
import psycopg2
import clickhouse_connect
import sys
import os

# Add the top-level 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Now import from utils and config
from src.utils.retry import retry_on_failure
from src.config.config import SUPABASE_DB, SUPABASE_USER, SUPABASE_PASSWORD, SUPABASE_HOST, SUPABASE_PORT, TIMEOUT, CLICKHOUSE_HOST, CLICKHOUSE_PORT, CLICKHOUSE_USER, CLICKHOUSE_PASSWORD, CLICKHOUSE_DB

TIMEOUT = 60000000000

@retry_on_failure
def connect_to_supabase():
    """Conecta ao Supabase PostgreSQL."""
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
        logging.error(f"Erro ao conectar ao Supabase: {e}")
        raise

@retry_on_failure
def connect_to_clickhouse():
    """Conecta ao ClickHouse."""
    logging.info("Connecting to ClickHouse...")
    try:
        client = clickhouse_connect.get_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DB,
            secure=True,
            verify=False
        )
        logging.info("Connection to ClickHouse established.")
        return client
    except Exception as e:
        logging.error(f"Erro ao conectar ao ClickHouse: {e}")
        raise