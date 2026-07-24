from fastapi import APIRouter

from app.services.websocket_manager import manager


router = APIRouter(
    prefix="/api/v1/websocket",
    tags=["websocket"]
)


@router.get("/status")
def websocket_status():

    streams = []

    for stream_name in manager.get_streams():

        streams.append(
            {
                "stream_name": stream_name,
                "clients": manager.get_connection_count(
                    stream_name
                )
            }
        )


    return {
        "code":0,
        "message":"success",
        "data":{
            "streams":streams
        }
    }