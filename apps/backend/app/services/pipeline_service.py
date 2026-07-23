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

from app.services.result_service import (
    result_service,
)

from app.services.detection_converter import (
    detection_converter,
)

from app.schemas.detection import DetectionResult


logger = logging.getLogger(__name__)


class PipelineService:

    """
    OpenEdge Vision 推理流水线。

    职责:

    1. 获取视频最新帧
    2. 调用 AI Plugin
    3. 返回检测结果
    """


    def infer(
        self,
        *,
        stream_name: str,
        plugin_id: str,
        frame_id: int | None = None,
    ) -> dict[str, Any]:


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
        # 3. Pipeline耗时
        #
        cost = (
            time.perf_counter()
            -
            start_time
        ) * 1000


        #
        # 4. 转换标准DetectionResult
        #
        if isinstance(result,DetectionResult):
            result.pipeline_time_ms=round (
                    cost,
                    3
            )
            standard_result=result
        else:
            standard_result=(
                    detection_converter.convert(
                        {
                            **result,
                            "pipeline_time_ms":
                                round(cost,3)
                        }
                    )
                )


        #
        # 5. 保存最新检测结果
        #
        result_service.update(
            standard_result
        )


        #
        # 保留Day7返回格式
        #
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
