import time
import logging

MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

def retry_on_failure(func):
    """Decorator to retry a function in case of failure."""
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                retries += 1
                logging.error(f"Error in {func.__name__}: {e}. Attempt {retries}/{MAX_RETRIES}")
                time.sleep(RETRY_DELAY)
        logging.critical(f"Critical failure: function {func.__name__} failed after {MAX_RETRIES} attempts.")
        raise Exception(f"Function {func.__name__} failed after {MAX_RETRIES} attempts.")
    return wrapper