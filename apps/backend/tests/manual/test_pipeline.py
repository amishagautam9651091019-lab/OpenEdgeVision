from app.services.pipeline_service import (
    pipeline_service,
)



result = pipeline_service.infer(
    stream_name="drone01",
    plugin_id="mock-detector",
)


print(result)