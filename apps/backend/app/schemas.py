from typing import Generic, TypeVar

from pydantic import BaseModel, Field


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    message: str = "success"
    data: T


class StreamInfo(BaseModel):
    name: str
    ready: bool = False

    source_type: str | None = None
    reader_count: int = 0

    tracks: list[str] = Field(default_factory=list)

    rtsp_url: str
    webrtc_url: str
    hls_url: str


class StreamSummary(BaseModel):
    total: int
    online: int
    offline: int
    streams: list[StreamInfo]