"""Read-only local API; no cloud, credentials, or production calibration claims."""
from __future__ import annotations
import asyncio
import json
import math
from uuid import UUID
from aiohttp import ClientError, ClientSession, ClientTimeout
from yarl import URL
from .const import METRICS, MODEL

class AudioPictureError(Exception):
    """Unavailable endpoint or invalid protocol data."""

def endpoint(host: str, port: int) -> URL:
    if not isinstance(host, str) or not host or any(c in host for c in "/@?#\\ \t\r\n"):
        raise AudioPictureError("Invalid device host")
    if isinstance(port, bool) or not isinstance(port, int) or not 1 <= port <= 65535:
        raise AudioPictureError("Invalid port")
    try:
        return URL.build(scheme="http", host=host, port=port)
    except (ValueError, TypeError) as err:
        raise AudioPictureError("Invalid device address") from err

def identity(data: dict) -> str:
    try:
        if not isinstance(data, dict) or type(data.get("api_version")) is not int or data["api_version"] != 1:
            raise ValueError("API version")
        value = data["uuid"]
        if not isinstance(value, str):
            raise ValueError("UUID type")
        return str(UUID(value))
    except (KeyError, ValueError, TypeError, AttributeError) as err:
        raise AudioPictureError("Invalid device identity") from err

class AudioPictureClient:
    def __init__(self, session: ClientSession, host: str, port: int = 80):
        self.session = session
        self.base = endpoint(host, port)

    async def _get(self, path: str) -> dict:
        try:
            async with self.session.get(self.base / "api" / "v1" / path,
                    timeout=ClientTimeout(total=5), allow_redirects=False) as response:
                if response.status != 200 or response.content_type != "application/json":
                    raise AudioPictureError("Unexpected HTTP response")
                # Never accept an unbounded response from a discovered device.
                chunks = bytearray()
                async for chunk in response.content.iter_chunked(4096):
                    chunks.extend(chunk)
                    if len(chunks) > 16384:
                        raise AudioPictureError("Response too large")
                data = json.loads(chunks)
                if not isinstance(data, dict):
                    raise AudioPictureError("Expected object")
                return data
        except (ClientError, asyncio.TimeoutError, ValueError, UnicodeError, RecursionError) as err:
            raise AudioPictureError("Device unavailable or malformed response") from err

    async def info(self) -> dict:
        data = await self._get("info")
        data["uuid"] = identity(data)
        if data.get("model") != MODEL or not isinstance(data.get("firmware"), str):
            raise AudioPictureError("Unsupported model")
        if not isinstance(data.get("capabilities"), dict):
            raise AudioPictureError("Missing capabilities")
        return data

    async def status(self, expected_uuid: str) -> dict:
        data = await self._get("status")
        if identity(data) != expected_uuid:
            raise AudioPictureError("Device identity changed")
        for key, (low, high) in METRICS.items():
            if key not in data:
                raise AudioPictureError("Incomplete sensor response")
            value = data[key]
            if value is not None and (type(value) not in (int, float)
                    or not low <= value <= high or not math.isfinite(value)):
                raise AudioPictureError("Invalid sensor value")
        return data
