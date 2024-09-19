import sys
import os
import logging
from tqdm import tqdm

# Add the top-level 'src' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import necessary modules
from src.utils.connections import connect_to_supabase, connect_to_clickhouse
from src.utils.clickhouse_utils import ensure_clickhouse_table, load_data_to_clickhouse, check_existing_records
from src.processing.data_extraction import list_supabase_tables, extract_data_from_supabase
from src.processing.data_cleaning import transform_data, remove_duplicates


def etl_process():
    """Executes the full ETL process."""
    conn = connect_to_supabase()
    clickhouse_client = connect_to_clickhouse()

    try:
        ensure_clickhouse_table(clickhouse_client)

        tables = list_supabase_tables(conn)
        for table_name in tables:
            # Check if records already exist in ClickHouse to avoid duplicates
            if check_existing_records(clickhouse_client, 'grupox', table_name):
                logging.info(f"Skipping table '{table_name}' as records with tag '{table_name}' already exist.")
                continue  # Skip this table if records already exist

            for batch_df in tqdm(extract_data_from_supabase(conn, table_name), desc=f"Processing table '{table_name}'"):
                transformed_df = transform_data(batch_df, table_name)
                transformed_df = remove_duplicates(transformed_df)  # Ensure duplicates are removed
                load_data_to_clickhouse(clickhouse_client, transformed_df)

        logging.info("All tables processed. Closing connections.")
    finally:
        conn.close()
        logging.info("ETL process completed successfully.")


if __name__ == "__main__":
    etl_process()