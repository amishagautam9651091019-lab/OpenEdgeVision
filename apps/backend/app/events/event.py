from dataclasses import dataclass, field
from typing import Any, Dict
import time
import uuid


@dataclass
class DetectionEvent:
    """
    AI检测事件模型

    用于 Pipeline -> EventBus -> Consumer
    """

    event_type: str

    stream_name: str

    plugin_id: str

    data: Dict[str, Any]

    event_id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    timestamp: float = field(
        default_factory=time.time
    )