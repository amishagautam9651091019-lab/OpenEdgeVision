from app.services.frame_provider_service import StreamConfig


DEFAULT_STREAMS = [
    StreamConfig(
        name="drone01",
        rtsp_url="rtsp://127.0.0.1:8554/drone01",
        enabled=True,
    ),
]