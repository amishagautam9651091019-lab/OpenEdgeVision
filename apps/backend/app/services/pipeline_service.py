from __future__ import annotations


import asyncio
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


from app.events import DetectionEvent


from app.events.runtime import (
    get_event_bus,
    get_loop,
)


logger = logging.getLogger(__name__)



class PipelineService:

    """
    OpenEdge Vision 推理流水线。

    Day10 AI Protocol v1.0版本。

    职责:

    1. 获取视频帧
    2. 调用AI Plugin
    3. Raw Result转换AI Protocol
    4. 保存结果
    5. 发布EventBus事件

    Plugin不负责协议生成。
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
        # 2. 调用AI Plugin
        #
        raw_result = (
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
        # 4. 统一转换AI Protocol v1.0
        #
        standard_result = (
            detection_converter.convert(

                {

                    **raw_result,


                    "pipeline_time_ms":

                        round(
                            cost,
                            3
                        )

                }

            )
        )



        #
        # 5. 保存最新结果
        #
        result_service.update(
            standard_result
        )



        #
        # 6. 发布AI Detection Event
        #
        event_bus = get_event_bus()


        if event_bus:


            event = DetectionEvent(

                event_type="detection",

                stream_name=stream_name,

                plugin_id=plugin_id,


                data=(
                    standard_result.model_dump()
                )

            )


            loop = get_loop()


            if loop:

                asyncio.run_coroutine_threadsafe(

                    event_bus.publish(
                        event
                    ),

                    loop

                )



        #
        # 7. API返回统一协议
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
                    3
                ),


            "result":

                standard_result.model_dump()

        }



pipeline_service = PipelineService()