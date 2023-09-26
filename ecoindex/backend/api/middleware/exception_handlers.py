from fastapi import Request, status
from fastapi.responses import JSONResponse


async def handle_screenshot_not_found_exception(_: Request, exc: FileNotFoundError):
    return JSONResponse(
        content={"detail": str(exc)},
        status_code=status.HTTP_404_NOT_FOUND,
    )
