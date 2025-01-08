from fastapi import HTTPException
from .logger import get_logger

logger = get_logger(__name__)

def raise_http_error(status_code: int, message: str):
    """Levanta uma exceção HTTP com logs."""
    logger.error(message)
    raise HTTPException(status_code=status_code, detail={"message": message, "status_code": status_code})
