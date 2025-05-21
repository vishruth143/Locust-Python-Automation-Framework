import json
from utilities.logger import setup_logger

logger = setup_logger()
def log_response(method, url, response, payload=None):
    log_message = (
        f"{method} {url} | Status: {response.status_code} | "
        f"Request: {json.dumps(payload) if payload else 'N/A'} | "
        f"Response: {response.text[:200]}..."  # Trim long responses
    )
    if response.status_code >= 400:
        logger.error(log_message)
    else:
        logger.info(log_message)