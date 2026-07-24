import asyncio
import logging

from typing import Dict, List

from fastapi import WebSocket


logger = logging.getLogger(__name__)


class WebSocketManager:

    def __init__(self):

        # 保存不同stream的视频客户端
        self.connections: Dict[
            str,
            List[WebSocket]
        ] = {}

        # FastAPI asyncio event loop
        self.loop = None


    async def connect(
        self,
        websocket: WebSocket,
        stream_name: str
    ):

        await websocket.accept()

        # 保存FastAPI主事件循环
        self.loop = asyncio.get_running_loop()


        if stream_name not in self.connections:

            self.connections[stream_name] = []


        self.connections[stream_name].append(
            websocket
        )


        logger.info(
            "WebSocket connected: stream=%s clients=%s",
            stream_name,
            len(self.connections[stream_name])
        )


    def disconnect(
        self,
        websocket: WebSocket,
        stream_name: str
    ):


        if stream_name in self.connections:

            if websocket in self.connections[stream_name]:

                self.connections[stream_name].remove(
                    websocket
                )


            # 没有客户端时删除stream
            if not self.connections[stream_name]:

                del self.connections[stream_name]


        logger.info(
            "WebSocket disconnected: stream=%s",
            stream_name
        )


    async def broadcast(
        self,
        stream_name: str,
        data: dict
    ):


        if stream_name not in self.connections:

            return


        dead_connections = []


        clients = list(
            self.connections[stream_name]
        )


        logger.debug(
            "Broadcast: stream=%s clients=%s",
            stream_name,
            len(clients)
        )


        for websocket in clients:

            try:

                await websocket.send_json(
                    data
                )


            except Exception as e:

                logger.warning(
                    "WebSocket send failed: %s",
                    e
                )

                dead_connections.append(
                    websocket
                )


        # 清理断开的连接
        for websocket in dead_connections:

            self.disconnect(
                websocket,
                stream_name
            )


    def get_connection_count(
        self,
        stream_name: str
    ) -> int:


        if stream_name not in self.connections:

            return 0


        return len(
            self.connections[stream_name]
        )


    def get_streams(self):

        return list(
            self.connections.keys()
        )


manager = WebSocketManager()