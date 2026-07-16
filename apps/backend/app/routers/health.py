from fastapi import APIRouter

from app.config import settings


router = APIRouter(
    prefix="/api/v1",
    tags=["System"],
)


@router.get("/health")
def health() -> dict:
    return {
        "code": 0,
        "message": "success",
        "data": {
            "service": settings.app_name,
            "version": settings.version,
            "status": "running",
        },
    }
