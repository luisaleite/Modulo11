# src/connectors/prometheus_connector.py
from prometheus_api_client import PrometheusConnect
import pandas as pd
import logging

def connect_to_prometheus(url='http://localhost:9090'):
    """Connect to Prometheus instance."""
    logging.info("Connecting to Prometheus...")
    try:
        prom = PrometheusConnect(url=url, disable_ssl=True)
        logging.info("Connected to Prometheus.")
        return prom
    except Exception as e:
        logging.error(f"Error connecting to Prometheus: {e}")
        raise

def fetch_prometheus_metrics(metric_name, start_time=None, end_time=None):
    """Fetch metrics from Prometheus."""
    prom = connect_to_prometheus()
    try:
        metrics_data = prom.get_current_metric_value(metric_name=metric_name)
        metrics_df = pd.json_normalize(metrics_data)
        return metrics_df
    except Exception as e:
        logging.error(f"Error fetching metrics from Prometheus: {e}")
        raise