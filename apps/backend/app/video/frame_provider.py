from __future__ import annotations

import logging
import threading
import time
from dataclasses import dataclass
from typing import Dict, Optional

import cv2
import numpy as np


logger = logging.getLogger(__name__)


@dataclass
class FrameSnapshot:
    """
    视频帧快照。

    frame:
        OpenCV BGR 图像。

    frame_id:
        当前会话累计读取成功的帧编号。

    timestamp:
        读取到该帧时的 Unix 时间戳。

    width / height:
        图像尺寸。
    """

    frame: np.ndarray
    frame_id: int
    timestamp: float
    width: int
    height: int


class StreamSession:
    """
    单路视频流读取会话。

    每个 StreamSession 使用一个后台线程持续读取 RTSP，
    只缓存最新一帧，避免推理请求每次重新连接视频流。
    """

    def __init__(
        self,
        stream_name: str,
        stream_url: str,
        reconnect_interval: float = 2.0,
        read_failure_limit: int = 30,
    ) -> None:
        self.stream_name = stream_name
        self.stream_url = stream_url
        self.reconnect_interval = reconnect_interval
        self.read_failure_limit = read_failure_limit

        self._capture: Optional[cv2.VideoCapture] = None
        self._thread: Optional[threading.Thread] = None

        self._running = False
        self._connected = False

        self._lock = threading.Lock()
        self._latest_snapshot: Optional[FrameSnapshot] = None

        self._frame_id = 0
        self._last_error: Optional[str] = None

    @property
    def running(self) -> bool:
        return self._running

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def last_error(self) -> Optional[str]:
        return self._last_error

    def start(self) -> None:
        """
        启动后台读取线程。
        """

        if self._running:
            logger.warning(
                "Stream session already running: %s",
                self.stream_name,
            )
            return

        self._running = True

        self._thread = threading.Thread(
            target=self._run,
            name=f"frame-provider-{self.stream_name}",
            daemon=True,
        )

        self._thread.start()

        logger.info(
            "Stream session started: name=%s url=%s",
            self.stream_name,
            self.stream_url,
        )

    def stop(self) -> None:
        """
        停止视频流读取并释放资源。
        """

        self._running = False

        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)

        self._release_capture()

        self._connected = False

        logger.info(
            "Stream session stopped: %s",
            self.stream_name,
        )

    def get_latest_frame(
        self,
        copy_frame: bool = True,
    ) -> Optional[FrameSnapshot]:
        """
        获取当前缓存的最新帧。

        copy_frame=True：
            返回图像副本，避免推理或绘制过程中修改共享缓存。
        """

        with self._lock:
            snapshot = self._latest_snapshot

            if snapshot is None:
                return None

            frame = (
                snapshot.frame.copy()
                if copy_frame
                else snapshot.frame
            )

            return FrameSnapshot(
                frame=frame,
                frame_id=snapshot.frame_id,
                timestamp=snapshot.timestamp,
                width=snapshot.width,
                height=snapshot.height,
            )

    def get_status(self) -> dict:
        """
        返回当前流会话状态。
        """

        snapshot = self.get_latest_frame(copy_frame=False)

        return {
            "stream_name": self.stream_name,
            "stream_url": self.stream_url,
            "running": self._running,
            "connected": self._connected,
            "frame_id": (
                snapshot.frame_id
                if snapshot is not None
                else None
            ),
            "last_frame_timestamp": (
                snapshot.timestamp
                if snapshot is not None
                else None
            ),
            "width": (
                snapshot.width
                if snapshot is not None
                else None
            ),
            "height": (
                snapshot.height
                if snapshot is not None
                else None
            ),
            "last_error": self._last_error,
        }

    def _run(self) -> None:
        """
        后台线程主循环。
        """

        consecutive_failures = 0

        while self._running:
            if self._capture is None or not self._capture.isOpened():
                if not self._open_capture():
                    time.sleep(self.reconnect_interval)
                    continue

            success, frame = self._capture.read()

            if not success or frame is None:
                consecutive_failures += 1

                self._last_error = (
                    f"Failed to read frame "
                    f"({consecutive_failures}/"
                    f"{self.read_failure_limit})"
                )

                if consecutive_failures >= self.read_failure_limit:
                    logger.warning(
                        "Too many frame read failures, reconnecting: %s",
                        self.stream_name,
                    )

                    self._connected = False
                    self._release_capture()
                    consecutive_failures = 0

                    time.sleep(self.reconnect_interval)
                else:
                    time.sleep(0.05)

                continue

            consecutive_failures = 0
            self._connected = True
            self._last_error = None
            self._frame_id += 1

            height, width = frame.shape[:2]

            snapshot = FrameSnapshot(
                frame=frame,
                frame_id=self._frame_id,
                timestamp=time.time(),
                width=width,
                height=height,
            )

            with self._lock:
                self._latest_snapshot = snapshot

        self._release_capture()

    def _open_capture(self) -> bool:
        """
        打开 RTSP 或其他 OpenCV 支持的视频源。
        """

        self._release_capture()

        logger.info(
            "Connecting to stream: name=%s url=%s",
            self.stream_name,
            self.stream_url,
        )

        capture = cv2.VideoCapture(
            self.stream_url,
            cv2.CAP_FFMPEG,
        )

        if not capture.isOpened():
            self._last_error = (
                f"Unable to open stream: {self.stream_url}"
            )

            logger.error(
                "Unable to open stream: name=%s url=%s",
                self.stream_name,
                self.stream_url,
            )

            capture.release()
            return False

        # 尽量降低缓存，减少实时视频延迟。
        capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self._capture = capture
        self._connected = True
        self._last_error = None

        logger.info(
            "Connected to stream: %s",
            self.stream_name,
        )

        return True

    def _release_capture(self) -> None:
        """
        释放 OpenCV VideoCapture。
        """

        if self._capture is not None:
            self._capture.release()
            self._capture = None


class FrameProvider:
    """
    多路视频流帧管理器。

    负责：

    - 创建 StreamSession
    - 启动和停止流读取
    - 管理多路视频流
    - 返回最新帧
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, StreamSession] = {}
        self._lock = threading.Lock()

    def add_stream(
        self,
        stream_name: str,
        stream_url: str,
        auto_start: bool = True,
    ) -> StreamSession:
        """
        添加视频流。

        若同名视频流已经存在，则直接返回原会话。
        """

        with self._lock:
            existing = self._sessions.get(stream_name)

            if existing is not None:
                if existing.stream_url != stream_url:
                    raise ValueError(
                        f"Stream '{stream_name}' already exists "
                        f"with another URL"
                    )

                return existing

            session = StreamSession(
                stream_name=stream_name,
                stream_url=stream_url,
            )

            self._sessions[stream_name] = session

        if auto_start:
            session.start()

        return session

    def remove_stream(self, stream_name: str) -> bool:
        """
        删除视频流并停止对应线程。
        """

        with self._lock:
            session = self._sessions.pop(
                stream_name,
                None,
            )

        if session is None:
            return False

        session.stop()
        return True

    def start_stream(self, stream_name: str) -> None:
        session = self._require_session(stream_name)
        session.start()

    def stop_stream(self, stream_name: str) -> None:
        session = self._require_session(stream_name)
        session.stop()

    def get_latest_frame(
        self,
        stream_name: str,
        copy_frame: bool = True,
    ) -> Optional[FrameSnapshot]:
        session = self._require_session(stream_name)

        return session.get_latest_frame(
            copy_frame=copy_frame,
        )

    def get_stream_status(self, stream_name: str) -> dict:
        session = self._require_session(stream_name)
        return session.get_status()

    def list_streams(self) -> list[dict]:
        with self._lock:
            sessions = list(self._sessions.values())

        return [
            session.get_status()
            for session in sessions
        ]

    def shutdown(self) -> None:
        """
        停止全部视频流。
        """

        with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()

        for session in sessions:
            session.stop()

    def _require_session(
        self,
        stream_name: str,
    ) -> StreamSession:
        with self._lock:
            session = self._sessions.get(stream_name)

        if session is None:
            raise KeyError(
                f"Stream session not found: {stream_name}"
            )

        return session


frame_provider = FrameProvider()