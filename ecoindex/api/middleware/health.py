from fastapi import FastAPI
from fastapi_health import health

from ecoindex.api.database.engine import is_database_online
from ecoindex.models import ApiHealth


def add_healthcheck_route(app: FastAPI) -> FastAPI:
    app.add_api_route(
        path="/health",
        endpoint=health([is_database_online]),
        tags=["Infra"],
        name="Get healthcheck",
        description="Check health status of components of the API (database...)",
        response_model=ApiHealth,
    )
