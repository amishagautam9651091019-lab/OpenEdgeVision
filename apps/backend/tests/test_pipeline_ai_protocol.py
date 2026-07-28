import pytest

from unittest.mock import MagicMock


from app.services.pipeline_service import (
    pipeline_service,
)


from app.services.frame_provider_service import (
    frame_provider_service,
)


from app.services.plugin_service import (
    plugin_service,
)


from app.events.event_bus import (
    EventBus,
)


from app.events import DetectionEvent



# =====================================================
# Mock FrameProvider
# =====================================================

def mock_frame(stream_name):

    """
    模拟FrameProvider

    对应真实接口:

    get_frame(stream_name)
    """


    snapshot = MagicMock()


    snapshot.stream_name = stream_name


    snapshot.frame_id = 1


    snapshot.frame = {

        "width":1920,

        "height":1080,

    }


    return snapshot



# =====================================================
# Plugin初始化
# =====================================================

def ensure_mock_plugin_loaded():

    """
    测试环境加载mock-detector

    等价生产环境:

    POST /plugins/mock-detector/load

    """


    try:

        plugin_service.load_plugin(
            "mock-detector"
        )

    except Exception:

        # 已经加载则忽略

        pass



# =====================================================
# Pipeline AI Protocol Test
# =====================================================

def test_pipeline_return_ai_protocol():


    #
    # 初始化插件
    #

    ensure_mock_plugin_loaded()



    #
    # Mock视频帧
    #

    frame_provider_service.get_frame = mock_frame



    result = pipeline_service.infer(

        stream_name="drone01",

        plugin_id="mock-detector"

    )



    assert result is not None



    ai_result = result["result"]



    assert (

        ai_result["version"]

        ==

        "1.0"

    )



    assert (

        ai_result["task_type"]

        ==

        "detection"

    )



    assert (

        ai_result["plugin_id"]

        ==

        "mock-detector"

    )



    assert "objects" in ai_result



    assert isinstance(

        ai_result["objects"],

        list

    )



# =====================================================
# EventBus AI Payload Test
# =====================================================

@pytest.mark.asyncio
async def test_detection_event_ai_payload():


    bus = EventBus()


    received=[]



    async def handler(event):

        received.append(event)



    bus.subscribe(

        "detection",

        handler

    )



    event = DetectionEvent(

        event_type="detection",

        stream_name="drone01",

        plugin_id="mock-detector",

        data={

            "version":"1.0",

            "task_type":"detection",

            "objects":[]

        }

    )



    await bus.publish(event)



    assert len(received)==1



    assert (

        received[0]

        .data["version"]

        ==

        "1.0"

    )


    assert (

        received[0]

        .data["task_type"]

        ==

        "detection"

    )


    assert (

        "objects"

        in

        received[0].data

    )