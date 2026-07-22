from __future__ import annotations


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


from app.services.pipeline_service import (
    pipeline_service,
)



router = APIRouter(
    prefix="/pipeline",
    tags=[
        "Pipeline"
    ],
)



class InferRequest(BaseModel):
    """
    推理请求参数。
    """

    stream_name: str

    plugin_id: str



@router.post("/infer")
def infer(
    request: InferRequest,
):

    try:

        result = (
            pipeline_service.infer(
                stream_name=request.stream_name,
                plugin_id=request.plugin_id,
            )
        )


    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc



    return {

        "code": 0,

        "message": "success",

        "data": result,

    }