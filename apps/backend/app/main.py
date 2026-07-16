from fastapi import FastAPI

from app.routers.health import router as health_router


app = FastAPI(
    title="OpenEdge Vision API",
    version="0.1.0",
    description="OpenEdge Vision Edge AI Platform",
)

app.include_router(health_router)


@app.get("/")
def root() -> dict:
    return {
        "name": "OpenEdge Vision",
        "version": "0.1.0",
        "status": "running",
    }
