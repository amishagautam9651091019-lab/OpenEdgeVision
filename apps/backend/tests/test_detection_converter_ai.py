"""
Day9 Step2
DetectionConverter -> AI Protocol v1.0 测试

验证：

Raw Detection Dict

        |

        |

DetectionConverter

        |

        |

app.schemas.ai.detection.DetectionResult


"""

import pytest


from app.services.detection_converter import (
    detection_converter,
)


from app.schemas.ai import (
    DetectionResult,
)



def test_detection_converter_to_ai_protocol():
    """
    测试 DetectionConverter 是否输出 AI DetectionResult v1.0
    """


    raw_result = {

        "stream_name": "drone01",

        "frame_id": 1,

        "timestamp": 123.0,

        "plugin_id": "mock-detector",


        "detections": [

            {

                "class_id": 0,

                "class_name": "person",

                "confidence": 0.9,

                "bbox": {

                    "x": 10,

                    "y": 20,

                    "width": 50,

                    "height": 80

                }

            }

        ],


        "inference_time_ms": 5,

        "pipeline_time_ms": 8

    }



    result = detection_converter.convert(
        raw_result
    )


    #
    # 1. 类型检查
    #
    assert isinstance(
        result,
        DetectionResult
    )


    #
    # 2. 基础协议检查
    #
    assert result.version == "1.0"

    assert result.task_type == "detection"

    assert result.stream_name == "drone01"

    assert result.frame_id == 1

    assert result.plugin_id == "mock-detector"



    #
    # 3. Detection对象检查
    #
    assert len(
        result.objects
    ) == 1



    obj = result.objects[0]


    assert obj.class_id == 0

    assert obj.class_name == "person"

    assert obj.confidence == 0.9



    #
    # 4. bbox检查
    #
    assert obj.bbox.x == 10

    assert obj.bbox.y == 20

    assert obj.bbox.width == 50

    assert obj.bbox.height == 80



    #
    # 5. Performance检查
    #
    assert result.performance is not None


    assert (
        result.performance.inference_ms
        == 5
    )


    assert (
        result.performance.pipeline_ms
        == 8
    )



def test_detection_converter_dump_json():

    """
    验证最终协议JSON结构
    """

    result = detection_converter.convert(

        {

            "stream_name": "drone01",

            "frame_id": 100,

            "timestamp": 123.5,

            "plugin_id": "mock",


            "detections": [],


            "inference_time_ms": 1

        }

    )


    data = result.model_dump()


    assert data["version"] == "1.0"

    assert data["task_type"] == "detection"


    assert (
        "objects"
        in data
    )


    assert (
        "performance"
        in data
    )