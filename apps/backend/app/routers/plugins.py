from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.plugin import MockPredictRequest
from app.services.plugin_service import plugin_service


router = APIRouter(
    prefix="/api/v1/plugins",
    tags=["AI Plugins"],
)


def success_response(data):
    return {
        "code": 0,
        "message": "success",
        "data": data,
    }


@router.get("")
def list_plugins():
    data = plugin_service.list_plugins()

    return success_response(
        data.model_dump(mode="json")
    )


@router.get("/{plugin_id}")
def get_plugin(plugin_id: str):
    try:
        plugin = plugin_service.get_plugin(plugin_id)

        return success_response(
            plugin.model_dump(mode="json")
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.post("/{plugin_id}/load")
def load_plugin(plugin_id: str):
    try:
        data = plugin_service.load_plugin(plugin_id)

        return success_response(
            data.model_dump(mode="json")
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Plugin load failed: {exc}",
        ) from exc


@router.post("/{plugin_id}/unload")
def unload_plugin(plugin_id: str):
    try:
        data = plugin_service.unload_plugin(plugin_id)

        return success_response(
            data.model_dump(mode="json")
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.get("/{plugin_id}/health")
def plugin_health(plugin_id: str):
    try:
        data = plugin_service.get_health(plugin_id)

        return success_response(
            data.model_dump(mode="json")
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


@router.post("/{plugin_id}/predict")
def mock_predict(
    plugin_id: str,
    request: MockPredictRequest,
):
    try:
        result = plugin_service.mock_predict(
            plugin_id=plugin_id,
            stream_name=request.stream_name,
            frame_id=request.frame_id,
            frame_width=request.frame_width,
            frame_height=request.frame_height,
        )

        return success_response(
            result.model_dump(mode="json")
        )

    except KeyError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Inference failed: {exc}",
        ) from exc