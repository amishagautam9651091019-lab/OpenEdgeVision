from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable

from app.video.frame_provider import frame_provider


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class StreamConfig:
    """
    FrameProvider 使用的视频流配置。
    """

    name: str
    rtsp_url: str
    enabled: bool = True


class FrameProviderService:
    """
    FrameProvider 应用层服务。

    负责：

    - 根据 Camera 配置启动视频流
    - 防止重复创建会话
    - 返回视频流运行状态
    - 在应用关闭时释放全部资源
    """

    def __init__(self) -> None:
        self._initialized = False

    @property
    def initialized(self) -> bool:
        return self._initialized

    def initialize(
        self,
        streams: Iterable[StreamConfig],
    ) -> None:
        """
        初始化全部启用的视频流。
        """

        if self._initialized:
            logger.warning(
                "FrameProviderService is already initialized"
            )
            return

        started_count = 0

        for stream in streams:
            if not stream.enabled:
                logger.info(
                    "Skipping disabled stream: %s",
                    stream.name,
                )
                continue

            try:
                frame_provider.add_stream(
                    stream_name=stream.name,
                    stream_url=stream.rtsp_url,
                    auto_start=True,
                )

                started_count += 1

                logger.info(
                    "Frame provider stream registered: "
                    "name=%s url=%s",
                    stream.name,
                    stream.rtsp_url,
                )

            except ValueError:
                logger.exception(
                    "Unable to register stream: %s",
                    stream.name,
                )

            except Exception:
                logger.exception(
                    "Unexpected error while starting stream: %s",
                    stream.name,
                )

        self._initialized = True

        logger.info(
            "FrameProviderService initialized, streams=%s",
            started_count,
        )

    def shutdown(self) -> None:
        """
        停止全部视频流。
        """

        if not self._initialized:
            return

        frame_provider.shutdown()
        self._initialized = False

        logger.info(
            "FrameProviderService shutdown completed"
        )

    def list_status(self) -> list[dict]:
        """
        返回所有 FrameProvider 会话状态。
        """

        return frame_provider.list_streams()

    def get_status(
        self,
        stream_name: str,
    ) -> dict:
        """
        返回单个视频流状态。
        """

        return frame_provider.get_stream_status(
            stream_name
        )

    def get_frame(
        self,
        stream_name:str,
    ):

        frame=(
        frame_provider.get_latest_frame(stream_name)
             )
        return frame


frame_provider_service = FrameProviderService()
