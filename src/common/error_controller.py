from fastapi import HTTPException, status


async def error_controller(request, exc):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Duplicate of unique key error')
