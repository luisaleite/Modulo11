import psycopg2
import psycopg2.extras
import os
import logging
from tqdm import tqdm
import sys
import os

# Now import from retry
from src.utils.retry import retry_on_failure


# Add the top-level 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import the necessary configuration variables
from src.config.config import SUPABASE_DB, SUPABASE_USER, SUPABASE_PASSWORD, SUPABASE_HOST, SUPABASE_PORT, PROCESSED_DATA_DIR


# from sconfig.config import SUPABASE_DB, SUPABASE_USER, SUPABASE_PASSWORD, SUPABASE_HOST, SUPABASE_PORT, PROCESSED_DATA_DIR

@retry_on_failure
def store_in_supabase(df, table_name, batch_size=25000):
    """Armazena dados no banco Supabase."""
    parquet_path = os.path.join(PROCESSED_DATA_DIR, f"{table_name}.parquet")
    df.to_parquet(parquet_path)

    conn = None
    try:
        conn = psycopg2.connect(
            dbname=SUPABASE_DB,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT
        )
        cursor = conn.cursor()
        schema_name = "private_schema"
        columns = ', '.join([f"{col} TEXT" for col in df.columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS {schema_name}.{table_name} ({columns});"
        cursor.execute(create_table_query)

        for i in tqdm(range(0, len(df), batch_size), desc=f"Upload {table_name} para Supabase"):
            batch_df = df.iloc[i:i + batch_size]
            values = batch_df.values.tolist()
            insert_query = f"INSERT INTO {schema_name}.{table_name} ({', '.join(df.columns)}) VALUES %s"
            psycopg2.extras.execute_values(cursor, insert_query, values, page_size=batch_size)

        conn.commit()
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        if conn:
            conn.rollback()
        logging.error(f"Erro ao armazenar dados no Supabase: {e}")
        raise
    finally:
        if conn:
            cursor.close()
            conn.close()

@retry_on_failure
def test_supabase_connection():
    """Testa a conexão com o Supabase."""
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=SUPABASE_DB,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT
        )
        logging.info("Conexão bem-sucedida com o Supabase PostgreSQL.")
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        logging.error(f"Falha na conexão com o Supabase PostgreSQL: {e}")
        raise
    finally:
        if conn:
            conn.close()