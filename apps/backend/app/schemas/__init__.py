"""
OpenEdge Vision API 数据模型统一导出模块。
"""

from app.schemas.stream import (
    ApiResponse,
    StreamInfo,
    StreamSummary,
)

from app.schemas.plugin import (
    BoundingBox,
    DetectionObject,
    DetectionResult,
    MockPredictRequest,
    PluginActionData,
    PluginDevice,
    PluginHealthData,
    PluginInfo,
    PluginListData,
    PluginStatus,
    PluginType,
)

__all__ = [
    # Stream schemas
    "ApiResponse",
    "StreamInfo",
    "StreamSummary",

    # AI plugin schemas
    "BoundingBox",
    "DetectionObject",
    "DetectionResult",
    "MockPredictRequest",
    "PluginActionData",
    "PluginDevice",
    "PluginHealthData",
    "PluginInfo",
    "PluginListData",
    "PluginStatus",
    "PluginType",
]