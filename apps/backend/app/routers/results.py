from fastapi import APIRouter

from app.services.result_service import result_service


router = APIRouter(
    prefix="/api/v1/results",
    tags=["results"]
)


@router.get("/{stream_name}")
def get_result(stream_name:str):

    result = result_service.get(
        stream_name
    )

    if result is None:
        return {
            "code":1,
            "message":"no result"
        }


    return {
        "code":0,
        "message":"success",
        "data":result
    }