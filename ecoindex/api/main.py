from fastapi import FastAPI

from ecoindex.api.config import get_settings
from ecoindex.api.database.engine import prisma
from ecoindex.api.middleware import apply_exception_handlers
from ecoindex.api.middleware.health import add_healthcheck_route
from ecoindex.api.routes import router

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
