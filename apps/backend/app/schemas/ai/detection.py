from pydantic import BaseModel

from .base import (
    BaseAIResult,
)



class BoundingBox(BaseModel):

    x: float

    y: float

    width: float

    height: float



class DetectionObject(BaseModel):

    class_id: int

    class_name: str

    confidence: float

    bbox: BoundingBox



class DetectionResult(
    BaseAIResult
):

    """
    AI目标检测统一协议
    """

    task_type: str = "detection"

    objects: list[DetectionObject] = []