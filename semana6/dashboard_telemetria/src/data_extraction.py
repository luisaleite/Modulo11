import logging
import pandas as pd
from connectors.supabase_connector import fetch_supabase_metrics
from connectors.clickhouse_connector import fetch_clickhouse_metrics

def fetch_all_metrics():
    """
    Fetches and combines metrics from Supabase and ClickHouse.
    Returns a combined DataFrame with metrics from both databases.
    """
    try:
        # Fetch metrics from Supabase
        logging.info("Fetching metrics from Supabase...")
        supabase_metrics = fetch_supabase_metrics()

        # Fetch metrics from ClickHouse
        logging.info("Fetching metrics from ClickHouse...")
        clickhouse_metrics = fetch_clickhouse_metrics()

        # Add source column to distinguish data
        supabase_metrics['source'] = 'Supabase'
        clickhouse_metrics['source'] = 'ClickHouse'

        # Combine the two DataFrames
        logging.info("Combining Supabase and ClickHouse metrics...")
        combined_metrics = pd.concat([supabase_metrics, clickhouse_metrics], ignore_index=True)

        logging.info("Metrics successfully combined.")
        return combined_metrics

    except Exception as e:
        logging.error(f"Error in fetching or combining metrics: {e}")
        raise

if __name__ == "__main__":
    # For testing purposes, you can run this script directly to see the combined data
    metrics_df = fetch_all_metrics()
    print(metrics_df)