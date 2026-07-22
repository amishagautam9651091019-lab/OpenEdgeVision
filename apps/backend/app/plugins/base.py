from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.schemas.plugin import (
    DetectionResult,
    PluginDevice,
    PluginInfo,
    PluginStatus,
    PluginType,
)


class BaseVisionPlugin(ABC):
    """
    OpenEdge Vision AI 插件抽象基类。

    所有 YOLO、RT-DETR、分类、分割和跟踪插件，
    后续都必须继承该基类。
    """

    plugin_id: str
    name: str
    version: str
    plugin_type: PluginType
    description: str

    def __init__(
        self,
        *,
        device: PluginDevice = PluginDevice.CPU,
        model_path: str | None = None,
    ) -> None:
        self.device = device
        self.model_path = model_path
        self.status = PluginStatus.AVAILABLE
        self.error_message: str | None = None

    @property
    def is_loaded(self) -> bool:
        return self.status == PluginStatus.LOADED

    @abstractmethod
    def load(self) -> None:
        """加载模型或初始化插件资源。"""

    @abstractmethod
    def unload(self) -> None:
        """卸载模型并释放资源。"""

    @abstractmethod
    def predict(
        self,
        *,
        frame: Any,
        stream_name: str,
        frame_id: int,
    ) -> DetectionResult:
        """执行一次推理。"""

    def health(self) -> dict[str, Any]:
        """返回插件健康状态。"""

        return {
            "plugin_id": self.plugin_id,
            "healthy": self.status != PluginStatus.ERROR,
            "status": self.status.value,
            "is_loaded": self.is_loaded,
            "device": self.device.value,
            "error_message": self.error_message,
        }

    def get_info(self) -> PluginInfo:
        """返回统一插件信息。"""

        return PluginInfo(
            id=self.plugin_id,
            name=self.name,
            version=self.version,
            type=self.plugin_type,
            status=self.status,
            device=self.device,
            description=self.description,
            model_path=self.model_path,
            error_message=self.error_message,
        )