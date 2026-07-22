from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class PluginType(str, Enum):
    """AI 插件类型。"""

    OBJECT_DETECTION = "object_detection"
    CLASSIFICATION = "classification"
    SEGMENTATION = "segmentation"
    TRACKING = "tracking"
    OCR = "ocr"
    OTHER = "other"


class PluginStatus(str, Enum):
    """AI 插件运行状态。"""

    AVAILABLE = "available"
    LOADING = "loading"
    LOADED = "loaded"
    ERROR = "error"
    DISABLED = "disabled"


class PluginDevice(str, Enum):
    """插件运行设备。"""

    CPU = "cpu"
    CUDA = "cuda"
    NPU = "npu"
    AUTO = "auto"


class BoundingBox(BaseModel):
    """检测框，使用左上角坐标加宽高。"""

    x: float = Field(..., ge=0)
    y: float = Field(..., ge=0)
    width: float = Field(..., ge=0)
    height: float = Field(..., ge=0)


class DetectionObject(BaseModel):
    """单个检测目标。"""

    class_id: int
    class_name: str
    confidence: float = Field(..., ge=0, le=1)
    bbox: BoundingBox


class DetectionResult(BaseModel):
    """统一推理结果。"""

    frame_id: int
    timestamp: float
    stream_name: str
    plugin_id: str
    inference_time_ms: float
    detections: list[DetectionObject]


class PluginInfo(BaseModel):
    """插件基本信息。"""

    id: str
    name: str
    version: str
    type: PluginType
    status: PluginStatus
    device: PluginDevice
    description: str = ""
    model_path: str | None = None
    input_width: int | None = None
    input_height: int | None = None
    class_count: int | None = None
    error_message: str | None = None
    created_at: datetime = Field(default_factory=datetime.now)


class PluginListData(BaseModel):
    """插件列表接口 data 部分。"""

    total: int
    loaded: int
    available: int
    plugins: list[PluginInfo]


class PluginActionData(BaseModel):
    """插件加载或卸载结果。"""

    plugin: PluginInfo


class PluginHealthData(BaseModel):
    """插件健康状态。"""

    plugin_id: str
    healthy: bool
    status: PluginStatus
    details: dict[str, Any] = Field(default_factory=dict)


class MockPredictRequest(BaseModel):
    """Mock 推理测试请求。"""

    stream_name: str = "drone01"
    frame_id: int = 1
    frame_width: int = Field(default=1280, gt=0)
    frame_height: int = Field(default=720, gt=0)