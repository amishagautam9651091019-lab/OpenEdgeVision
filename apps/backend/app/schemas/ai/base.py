from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ModelInfo(BaseModel):

    name: Optional[str] = None

    version: Optional[str] = None


class PerformanceInfo(BaseModel):

    capture_ms: float = 0

    preprocess_ms: float = 0

    inference_ms: float = 0

    postprocess_ms: float = 0

    pipeline_ms: float = 0



class BaseAIResult(BaseModel):

    """
    AI统一结果基础协议 v1.0
    """

    version: str = "1.0"

    task_type: str

    stream_name: str

    frame_id: int

    timestamp: float

    plugin_id: str

    model: ModelInfo | None = None

    performance: PerformanceInfo | None = None