import logging

logger = logging.getLogger("google_maps_provider")
logger.setLevel(logging.INFO)

class ProviderLogger:
    @staticmethod
    def log_started(query: str):
        logger.info(f"Search Started: {query}")

    @staticmethod
    def log_finished(query: str, duration: float, count: int):
        logger.info(f"Search Finished: {query} in {duration:.2f}s, found {count}")

    @staticmethod
    def log_error(error: str):
        logger.error(f"Provider Error: {error}")

    @staticmethod
    def log_retry(attempt: int, error: str):
        logger.warning(f"Retry {attempt} due to: {error}")

    @staticmethod
    def log_rate_limit():
        logger.warning("Rate limit hit.")
