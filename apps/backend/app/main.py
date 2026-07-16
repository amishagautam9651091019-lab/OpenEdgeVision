from fastapi import FastAPI

from app.config import settings
from app.routers.health import router as health_router
from app.routers.streams import router as streams_router


app = FastAPI(
    title="OpenEdge Vision API",
    version=settings.version,
    description=(
        "OpenEdge Vision edge AI platform backend API"
    ),
)

app.include_router(health_router)
app.include_router(streams_router)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    return {
        "name": "OpenEdge Vision",
        "version": settings.version,
        "status": "running",
    }