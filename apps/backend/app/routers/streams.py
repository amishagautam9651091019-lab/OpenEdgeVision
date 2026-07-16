from typing import Any

from fastapi import APIRouter, HTTPException, status

from app.schemas import ApiResponse, StreamInfo, StreamSummary
from app.services.mediamtx import (
    MediaMTXResponseError,
    MediaMTXUnavailableError,
    mediamtx_client,
)


router = APIRouter(
    prefix="/api/v1/streams",
    tags=["Streams"],
)


def _extract_source_type(item: dict[str, Any]) -> str | None:
    source = item.get("source")

    if isinstance(source, dict):
        source_type = source.get("type")

        if source_type is not None:
            return str(source_type)

    return None


def _extract_reader_count(item: dict[str, Any]) -> int:
    readers = item.get("readers")

    if isinstance(readers, list):
        return len(readers)

    return 0


def _extract_tracks(item: dict[str, Any]) -> list[str]:
    tracks = item.get("tracks")

    if not isinstance(tracks, list):
        return []

    result: list[str] = []

    for track in tracks:
        if isinstance(track, str):
            result.append(track)
        elif isinstance(track, dict):
            codec = track.get("codec")
            result.append(str(codec or track.get("type") or "unknown"))
        else:
            result.append(str(track))

    return result


def _to_stream_info(item: dict[str, Any]) -> StreamInfo:
    name = str(item.get("name", ""))

    return StreamInfo(
        name=name,
        ready=bool(item.get("ready", False)),
        source_type=_extract_source_type(item),
        reader_count=_extract_reader_count(item),
        tracks=_extract_tracks(item),
        rtsp_url=f"rtsp://127.0.0.1:8554/{name}",
        webrtc_url=f"http://127.0.0.1:8889/{name}",
        hls_url=f"http://127.0.0.1:8888/{name}",
    )


@router.get(
    "",
    response_model=ApiResponse[StreamSummary],
    summary="List video streams",
)
async def list_streams() -> ApiResponse[StreamSummary]:
    try:
        paths = await mediamtx_client.list_paths()

    except MediaMTXUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": 1001,
                "message": str(exc),
            },
        ) from exc

    except MediaMTXResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "code": 1002,
                "message": str(exc),
            },
        ) from exc

    streams = [
        _to_stream_info(item)
        for item in paths
        if item.get("name")
    ]

    # 输出顺序固定，方便前端和测试。
    streams.sort(key=lambda stream: stream.name)

    online = sum(1 for stream in streams if stream.ready)
    total = len(streams)

    return ApiResponse(
        data=StreamSummary(
            total=total,
            online=online,
            offline=total - online,
            streams=streams,
        )
    )


@router.get(
    "/{stream_name}",
    response_model=ApiResponse[StreamInfo],
    summary="Get one video stream",
)
async def get_stream(
    stream_name: str,
) -> ApiResponse[StreamInfo]:
    try:
        paths = await mediamtx_client.list_paths()

    except MediaMTXUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "code": 1001,
                "message": str(exc),
            },
        ) from exc

    except MediaMTXResponseError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={
                "code": 1002,
                "message": str(exc),
            },
        ) from exc

    for item in paths:
        if item.get("name") == stream_name:
            return ApiResponse(
                data=_to_stream_info(item)
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "code": 1004,
            "message": f"Stream '{stream_name}' was not found",
        },
    )