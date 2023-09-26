from fastapi import FastAPI


def apply_exception_handlers(app: FastAPI) -> None:
    """Apply exception handlers to the FastAPI app.

    Args:
        app (FastAPI): FastAPI app

    Returns:
        FastAPI: FastAPI app with exception handlers applied
    """
    from ecoindex.backend.api.middleware.exception_handlers import (
        handle_screenshot_not_found_exception,
    )

    app.add_exception_handler(RuntimeError, handle_screenshot_not_found_exception)
