from typing import Any

import httpx

from app.config import settings


class MediaMTXError(Exception):
    """Base exception for MediaMTX client errors."""


class MediaMTXUnavailableError(MediaMTXError):
    """Raised when MediaMTX cannot be reached."""


class MediaMTXResponseError(MediaMTXError):
    """Raised when MediaMTX returns an invalid response."""


class MediaMTXClient:
    """Small async client for the MediaMTX Control API."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout_seconds: float | None = None,
    ) -> None:
        self.base_url = (
            base_url or settings.mediamtx_api_url
        ).rstrip("/")

        self.timeout_seconds = (
            timeout_seconds
            if timeout_seconds is not None
            else settings.mediamtx_timeout_seconds
        )

    async def list_paths(self) -> list[dict[str, Any]]:
        """Return all MediaMTX paths."""

        url = f"{self.base_url}/v3/paths/list"

        try:
            async with httpx.AsyncClient(
                timeout=self.timeout_seconds
            ) as client:
                response = await client.get(url)

            response.raise_for_status()

        except httpx.ConnectError as exc:
            raise MediaMTXUnavailableError(
                f"Unable to connect to MediaMTX at {self.base_url}"
            ) from exc

        except httpx.TimeoutException as exc:
            raise MediaMTXUnavailableError(
                "MediaMTX request timed out"
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise MediaMTXResponseError(
                f"MediaMTX returned HTTP "
                f"{exc.response.status_code}"
            ) from exc

        try:
            payload = response.json()
        except ValueError as exc:
            raise MediaMTXResponseError(
                "MediaMTX returned invalid JSON"
            ) from exc

        items = payload.get("items")

        if items is None:
            return []

        if not isinstance(items, list):
            raise MediaMTXResponseError(
                "MediaMTX response field 'items' is not a list"
            )

        return items


mediamtx_client = MediaMTXClient()