from fastapi import APIRouter, WebSocket
import asyncio
import logging

from app.services.websocket_manager import manager


logger = logging.getLogger(__name__)


router = APIRouter()


@router.websocket(
    "/ws/streams/{stream_name}"
)
async def stream_result(
    websocket: WebSocket,
    stream_name: str,
):

    await manager.connect(
        websocket,
        stream_name
    )


    logger.info(
        f"WebSocket connected: {stream_name}"
    )


    try:

        while True:

            # 保持WebSocket连接
            # 后续由ResultService主动广播结果

            await asyncio.sleep(
                1
            )


    except Exception as e:

        logger.info(
            f"WebSocket closed: {stream_name}"
        )


    finally:

        manager.disconnect(
            websocket,
            stream_name
        )