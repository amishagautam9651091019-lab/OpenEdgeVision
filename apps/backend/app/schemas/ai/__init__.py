from .base import (
    BaseAIResult,
    ModelInfo,
    PerformanceInfo,
)


from .detection import (
    DetectionResult,
    DetectionObject,
    BoundingBox,
)


__all__ = [

    "BaseAIResult",

    "ModelInfo",

    "PerformanceInfo",

    "DetectionResult",

    "DetectionObject",

    "BoundingBox",

]