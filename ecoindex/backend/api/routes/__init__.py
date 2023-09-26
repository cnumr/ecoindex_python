import os
from importlib import import_module

from fastapi import APIRouter

router = APIRouter()


for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and not file.startswith("__"):
        router.include_router(
            import_module(
                f"ecoindex.backend.api.routes.{file.replace('.py', '')}"
            ).router
        )
