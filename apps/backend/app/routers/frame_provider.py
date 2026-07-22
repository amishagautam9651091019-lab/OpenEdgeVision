from __future__ import annotations


from fastapi import APIRouter, HTTPException


from app.services.frame_provider_service import (
    frame_provider_service,
)



router = APIRouter(
    prefix="/frame-provider",
    tags=[
        "Frame Provider"
    ],
)



@router.get("/streams")
def list_streams():
    """
    获取所有 FrameProvider 视频流状态。
    """

    return {
        "code": 0,
        "message": "success",
        "data": {
            "streams":
                frame_provider_service.list_status()
        },
    }



@router.get("/streams/{stream_name}")
def get_stream_status(
    stream_name: str,
):
    """
    获取指定视频流状态。
    """

    try:

        data = (
            frame_provider_service.get_status(
                stream_name
            )
        )


    except KeyError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc



    return {
        "code": 0,
        "message": "success",
        "data": data,
    }



@router.post("/streams/{stream_name}/start")
def start_stream(
    stream_name: str,
):
    """
    启动指定视频流读取。
    """

    try:

        from app.video.frame_provider import (
            frame_provider,
        )


        frame_provider.start_stream(
            stream_name
        )


    except KeyError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc



    return {
        "code":0,
        "message":"stream started",
        "data":{
            "stream_name":stream_name
        },
    }



@router.post("/streams/{stream_name}/stop")
def stop_stream(
    stream_name: str,
):
    """
    停止指定视频流读取。
    """

    try:

        from app.video.frame_provider import (
            frame_provider,
        )


        frame_provider.stop_stream(
            stream_name
        )


    except KeyError as exc:

        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc



    return {
        "code":0,
        "message":"stream stopped",
        "data":{
            "stream_name":stream_name
        },
    }