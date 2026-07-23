import asyncio
from typing import Dict, List

from fastapi import WebSocket


class WebSocketManager:


    def __init__(self):

        # 保存不同stream的视频客户端
        self.connections: Dict[
            str,
            List[WebSocket]
        ] = {}
        self.loop=None



    async def connect(
        self,
        websocket: WebSocket,
        stream_name: str
    ):

        await websocket.accept()

        self.loop=asyncio.get_running_loop()


        if stream_name not in self.connections:

            self.connections[stream_name] = []


        self.connections[stream_name].append(
            websocket
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



    async def broadcast(
        self,
        stream_name: str,
        data: dict
    ):


        if stream_name not in self.connections:
            return


        dead_connections = []


        for websocket in self.connections[stream_name]:

            try:

                await websocket.send_json(
                    data
                )


            except Exception:

                dead_connections.append(
                    websocket
                )



        # 清理断开的连接
        for websocket in dead_connections:

            self.disconnect(
                websocket,
                stream_name
            )



manager = WebSocketManager()
