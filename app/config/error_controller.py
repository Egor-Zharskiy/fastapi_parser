from fastapi import HTTPException, status
import logging
logger = logging.getLogger('Error controller')

async def error_controller(request, exc):
    logger.error(exc)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Duplicate of unique key error')
