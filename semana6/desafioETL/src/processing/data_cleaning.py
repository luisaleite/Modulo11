import logging
import pandas as pd
from tqdm import tqdm
import json


def clean_data(df):
    """Cleans the data by removing null values."""
    logging.info("Cleaning data...")
    with tqdm(total=len(df), desc="Cleaning data") as pbar:
        df.dropna(inplace=True)
        pbar.update(len(df))
    return df


def normalize_data(df):
    """Normalizes data with standard formatting."""
    logging.info("Normalizing data...")
    with tqdm(total=len(df), desc="Normalizing data") as pbar:
        df = df.applymap(lambda x: x.lower() if isinstance(x, str) else x)
        for col in df.select_dtypes(include=['datetime']):
            df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')
        pbar.update(len(df))
    return df


def aggregate_data(df):
    """Aggregates data as needed."""
    logging.info("Aggregating data...")
    with tqdm(total=len(df), desc="Aggregating data") as pbar:
        if 'category' in df.columns and 'amount' in df.columns:
            df = df.groupby('category', as_index=False)['amount'].sum()
        pbar.update(len(df))
    return df


def filter_data(df):
    """Filters data based on established conditions."""
    logging.info("Filtering data...")
    with tqdm(total=len(df), desc="Filtering data") as pbar:
        if 'status' in df.columns:
            df = df[df['status'] == 'active']
        pbar.update(len(df))
    return df


def convert_data_types(df):
    """Converts data types as necessary."""
    logging.info("Converting data types...")
    with tqdm(total=len(df), desc="Converting data types") as pbar:
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col])
                except ValueError:
                    continue
        for col in df.columns:
            if 'date' in col:
                df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)
        pbar.update(len(df))
    return df


def remove_duplicates(df):
    """Removes duplicate records."""
    logging.info("Removing duplicates...")
    with tqdm(total=len(df), desc="Removing duplicates") as pbar:
        df.drop_duplicates(inplace=True)
        pbar.update(len(df))
    return df




def map_fields(df):
    """Maps column fields as specified."""
    logging.info("Mapping fields...")
    with tqdm(total=len(df), desc="Mapping fields") as pbar:
        column_mapping = {'old_column_name': 'new_column_name'}
        df.rename(columns=column_mapping, inplace=True)
        pbar.update(len(df))
    return df


def validate_data(df):
    """Validates the data based on specific criteria."""
    logging.info("Validating data...")
    with tqdm(total=len(df), desc="Validating data") as pbar:
        if 'amount' in df.columns:
            df = df[df['amount'].between(0, 1000000)]
        pbar.update(len(df))
    return df


def transform_data(df, table_name):
    """Applies all transformations and adds metadata."""
    logging.info("Starting data transformation...")
    df = clean_data(df)
    df = normalize_data(df)
    df = aggregate_data(df)
    df = filter_data(df)
    df = convert_data_types(df)
    df = remove_duplicates(df)
    df = map_fields(df)
    df = validate_data(df)

    df['data'] = df.apply(lambda x: json.dumps(x.to_dict()).replace("'", "\\'"), axis=1)
    df['tag'] = table_name

    if 'date_time' not in df.columns:
        df['date_time'] = pd.to_datetime('now')

    df = df[['data', 'date_time', 'tag']]
    logging.info("Data transformation completed.")
    return df