import logging
from tqdm import tqdm

def ensure_clickhouse_table(client):
    """Ensures the ClickHouse table 'grupox' exists with the correct schema."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS grupox (
        data String,
        date_time DateTime,
        tag String
    ) ENGINE = MergeTree()
    ORDER BY date_time;
    """
    try:
        client.command(create_table_query)
        logging.info("Ensured ClickHouse table 'grupox' exists with correct schema.")
    except Exception as e:
        logging.error(f"Error ensuring table in ClickHouse: {e}")
        raise


def check_existing_records(client, table_name, tag):
    """Check if records with the given tag already exist in the table."""
    logging.info(f"Checking if records with tag '{tag}' already exist in '{table_name}'...")
    query = f"SELECT COUNT(*) FROM {table_name} WHERE tag = '{tag}'"
    result = client.command(query)
    return result > 0  # If records exist, return True


def load_data_to_clickhouse(client, df):
    """Loads the transformed data into ClickHouse."""
    logging.info("Loading data into ClickHouse...")
    try:
        data_tuples = list(df.itertuples(index=False, name=None))
        insert_query = """
        INSERT INTO grupox (data, date_time, tag)
        VALUES
        """
        values = ', '.join(
            f"('{data}', '{date_time}', '{tag}')" for (data, date_time, tag) in data_tuples
        )
        full_query = f"{insert_query} {values};"
        with tqdm(total=len(df), desc="Loading data to ClickHouse") as pbar:
            client.command(full_query)
            pbar.update(len(df))
        logging.info("Data loaded into ClickHouse.")
    except Exception as e:
        logging.error(f"Error loading data into ClickHouse: {e}")
        raise