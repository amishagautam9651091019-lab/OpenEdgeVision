from __future__ import annotations

import random
import time
from typing import Any

from app.plugins.base import BaseVisionPlugin
from app.plugins.registry import plugin_registry
from app.schemas.plugin import (
    BoundingBox,
    DetectionObject,
    DetectionResult,
    PluginDevice,
    PluginStatus,
    PluginType,
)


class MockDetectorPlugin(BaseVisionPlugin):
    """
    OpenEdge Vision Mock Detector Plugin.

    用于验证：

    - Plugin Registry
    - Plugin Lifecycle
    - REST API
    - DetectionResult 数据结构
    - AI Plugins 前端展示

    不依赖：
    - PyTorch
    - CUDA
    - ONNX
    - TensorRT
    """

    plugin_id = "mock-detector"
    name = "Mock Object Detector"
    version = "0.1.0"
    plugin_type = PluginType.OBJECT_DETECTION
    description = "用于验证 OpenEdge Vision AI 插件框架的模拟检测器"

    def __init__(
        self,
        *,
        device: PluginDevice = PluginDevice.CPU,
    ) -> None:
        super().__init__(device=device)

        self.config: dict[str, Any] = {
            "confidence_threshold": 0.5,
            "min_box_width": 80,
            "max_box_width": 240,
            "min_box_height": 80,
            "max_box_height": 220,
        }

    def load(self) -> None:
        """
        加载插件。

        Mock 插件只模拟初始化过程。
        """
        try:
            self.status = PluginStatus.LOADING

            time.sleep(0.05)

            self.error_message = None
            self.status = PluginStatus.LOADED

        except Exception as exc:
            self.error_message = str(exc)
            self.status = PluginStatus.ERROR
            raise

    def unload(self) -> None:
        """卸载插件资源。"""
        self.error_message = None
        self.status = PluginStatus.AVAILABLE

    def predict(
        self,
        frame: Any,
        *,
        frame_id: int = 0,
        stream_name: str = "unknown",
    ) -> DetectionResult:
        """
        模拟目标检测。
        """
        if not self.is_loaded:
            raise RuntimeError(
                f"Plugin {self.plugin_id} is not loaded"
            )

        start_time = time.perf_counter()

        width, height = self._get_frame_size(frame)

        box_width = random.randint(
            self.config["min_box_width"],
            self.config["max_box_width"],
        )

        box_height = random.randint(
            self.config["min_box_height"],
            self.config["max_box_height"],
        )

        box_width = min(box_width, max(width - 1, 1))
        box_height = min(box_height, max(height - 1, 1))

        max_x = max(width - box_width, 0)
        max_y = max(height - box_height, 0)

        x = random.randint(0, max_x) if max_x > 0 else 0
        y = random.randint(0, max_y) if max_y > 0 else 0

        confidence = round(
            random.uniform(
                self.config["confidence_threshold"],
                0.99,
            ),
            3,
        )

        detection = DetectionObject(
            class_id=0,
            class_name="mock-target",
            confidence=confidence,
            bbox=BoundingBox(
                x=x,
                y=y,
                width=box_width,
                height=box_height,
            ),
        )

        inference_time_ms = (
            time.perf_counter() - start_time
        ) * 1000

        return DetectionResult(
            frame_id=frame_id,
            timestamp=time.time(),
            stream_name=stream_name,
            plugin_id=self.plugin_id,
            inference_time_ms=round(
                inference_time_ms,
                3,
            ),
            detections=[detection],
        )

    @staticmethod
    def _get_frame_size(
        frame: Any,
    ) -> tuple[int, int]:
        """
        获取输入图像尺寸。

        OpenCV/NumPy 图像 shape 通常是：
        (height, width, channels)
        """
        shape = getattr(frame, "shape", None)

        if shape is None or len(shape) < 2:
            return 1280, 720

        width = int(shape[1])
        height = int(shape[0])

        if width <= 0 or height <= 0:
            return 1280, 720

        return width, height


plugin_registry.register(
    MockDetectorPlugin(),
    replace=True,
)