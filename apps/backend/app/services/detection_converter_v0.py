from app.schemas.detection import (
    DetectionResult,
    DetectionObject,
    BoundingBox,
    PerformanceInfo
)


class DetectionConverter:


    @staticmethod
    def convert(
        result: dict
    ) -> DetectionResult:


        objects = []


        for det in result.get(
            "detections",
            []
        ):

            objects.append(
                DetectionObject(
                    class_id=det["class_id"],

                    class_name=det["class_name"],

                    confidence=det["confidence"],

                    bbox=BoundingBox(
                        x=det["bbox"]["x"],
                        y=det["bbox"]["y"],
                        width=det["bbox"]["width"],
                        height=det["bbox"]["height"]
                    )
                )
            )


        return DetectionResult(

            stream_name=result["stream_name"],

            frame_id=result["frame_id"],

            timestamp=result["timestamp"],

            plugin_id=result["plugin_id"],

            objects=objects,

            performance=PerformanceInfo(

                inference_ms=
                result.get(
                    "inference_time_ms",
                    0
                ),

                pipeline_ms=
                result.get(
                    "pipeline_time_ms",
                    0
                )
            )
        )



detection_converter = DetectionConverter()