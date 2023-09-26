from fastapi import FastAPI

from ecoindex.backend.api.middleware import apply_exception_handlers
from ecoindex.backend.api.middleware.health import add_healthcheck_route
from ecoindex.backend.api.routes import router
from ecoindex.backend.config import get_settings
from ecoindex.backend.database.engine import prisma

settings = get_settings()


app = FastAPI(
    debug=settings.DEBUG,
    title="Ecoindex API",
    version="1.0.0",
    description=(
        "Ecoindex API enables you to perform ecoindex analysis of given web pages"
    ),
)


@app.on_event(event_type="startup")
async def on_startup():
    await prisma.connect()


@app.on_event(event_type="shutdown")
async def on_shutdown():
    await prisma.disconnect()


apply_exception_handlers(app=app)
add_healthcheck_route(app=app)

app.include_router(router)
