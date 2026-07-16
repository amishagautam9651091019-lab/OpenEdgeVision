from typing import Any

from app.schemas import StreamInfo, StreamSummary
from app.services.mediamtx import mediamtx_client


class StreamService:
    """Convert MediaMTX runtime data into platform stream models."""

    @staticmethod
    def _source_type(item: dict[str, Any]) -> str | None:
        source = item.get("source")

        if isinstance(source, dict):
            value = source.get("type")
            return str(value) if value is not None else None

        return None

    @staticmethod
    def _reader_count(item: dict[str, Any]) -> int:
        readers = item.get("readers")
        return len(readers) if isinstance(readers, list) else 0

    @staticmethod
    def _tracks(item: dict[str, Any]) -> list[str]:
        tracks = item.get("tracks")

        if not isinstance(tracks, list):
            return []

        result: list[str] = []

        for track in tracks:
            if isinstance(track, str):
                result.append(track)
            elif isinstance(track, dict):
                result.append(
                    str(
                        track.get("codec")
                        or track.get("type")
                        or "unknown"
                    )
                )

        return result

    @staticmethod
    def _to_stream(item: dict[str, Any]) -> StreamInfo:
        name = str(item.get("name", ""))

        return StreamInfo(
            name=name,
            ready=bool(item.get("ready", False)),
            source_type=StreamService._source_type(item),
            reader_count=StreamService._reader_count(item),
            tracks=StreamService._tracks(item),
            rtsp_url=f"rtsp://127.0.0.1:8554/{name}",
            webrtc_url=f"http://127.0.0.1:8889/{name}",
            hls_url=f"http://127.0.0.1:8888/{name}",
        )

    async def list_streams(self) -> StreamSummary:
        paths = await mediamtx_client.list_paths()

        streams = [
            self._to_stream(item)
            for item in paths
            if item.get("name")
        ]

        streams.sort(key=lambda stream: stream.name)

        online = sum(1 for stream in streams if stream.ready)
        total = len(streams)

        return StreamSummary(
            total=total,
            online=online,
            offline=total - online,
            streams=streams,
        )

    async def get_stream(self, stream_name: str) -> StreamInfo | None:
        summary = await self.list_streams()

        for stream in summary.streams:
            if stream.name == stream_name:
                return stream

        return None


stream_service = StreamService()