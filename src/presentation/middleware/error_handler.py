from fastapi import Request, status
from fastapi.responses import JSONResponse
from src.infrastructure.config import logger


async def error_handler_middleware(request: Request, call_next):
    """Middleware for handling errors globally."""
    try:
        return await call_next(request)
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(e)}
        )
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )
