from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


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


class PerformanceInfo(BaseModel):
    capture_ms: float = 0
    inference_ms: float = 0
    pipeline_ms: float = 0


class DetectionResult(BaseModel):
    stream_name: str

    frame_id: int

    timestamp: float

    plugin_id: str

    inference_time_ms:float =0

    detections: List[DetectionObject]

    pipeline_time_ms: float =0

