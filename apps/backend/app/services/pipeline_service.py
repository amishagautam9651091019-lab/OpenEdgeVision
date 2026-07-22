from __future__ import annotations


import logging
import time
from typing import Any


from app.services.frame_provider_service import (
    frame_provider_service,
)

from app.services.plugin_service import (
    plugin_service,
)


logger = logging.getLogger(__name__)


class PipelineService:
    """
    OpenEdge Vision 推理流水线。

    职责:

    1. 获取视频最新帧
    2. 调用 AI Plugin
    3. 返回检测结果

    不负责:

    - 视频读取
    - 插件管理
    - 模型加载
    """



    def infer(
        self,
        *,
        stream_name: str,
        plugin_id: str,
        frame_id: int | None = None,
    ) -> dict[str, Any]:
        """
        执行一次推理。

        Args:

            stream_name:
                视频流名称

            plugin_id:
                AI插件ID

            frame_id:
                可选指定帧编号

        """

        start_time = time.perf_counter()


        #
        # 1. 获取最新视频帧
        #
        snapshot = (
            frame_provider_service
            .get_frame(
                stream_name
            )
        )


        if snapshot is None:

            raise RuntimeError(
                f"No frame available "
                f"from stream {stream_name}"
            )


        #
        # 2. 调用 Plugin
        #
        result = (
            plugin_service.predict(
                plugin_id=plugin_id,
                frame=snapshot.frame,
                frame_id=snapshot.frame_id,
                stream_name=stream_name,
            )
        )


        #
        # 3. 补充 Pipeline 信息
        #
        cost = (
            time.perf_counter()
            -
            start_time
        ) * 1000


        return {

            "stream_name":
                stream_name,


            "plugin_id":
                plugin_id,


            "frame_id":
                snapshot.frame_id,


            "pipeline_time_ms":
                round(
                    cost,
                    3,
                ),


            "result":
                result,
        }



pipeline_service = PipelineService()