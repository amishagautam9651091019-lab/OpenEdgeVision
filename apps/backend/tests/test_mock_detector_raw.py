from app.plugins.builtin.mock_detector import (
    MockDetectorPlugin
)



def test_mock_detector_raw_output():


    plugin = MockDetectorPlugin()


    #
    # 模拟真实生命周期
    #
    plugin.load()



    result = plugin.predict(

        frame=None,

        frame_id=1,

        stream_name="drone01"

    )



    assert isinstance(
        result,
        dict
    )


    assert (
        "detections"
        in result
    )


    assert (
        "inference_time_ms"
        in result
    )


    assert len(
        result["detections"]
    ) == 1



    detection = (
        result["detections"][0]
    )


    assert (
        detection["class_name"]
        ==
        "mock-target"
    )


    #
    # 清理
    #
    plugin.unload()