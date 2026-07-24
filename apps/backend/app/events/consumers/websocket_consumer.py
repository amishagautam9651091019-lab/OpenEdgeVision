import logging

from app.events import DetectionEvent


logger = logging.getLogger(__name__)


class WebSocketConsumer:
    """
    WebSocket事件消费者

    EventBus Consumer

    职责:

    DetectionEvent
            |
            |
            v

    WebSocket消息

            |
            |
            v

    WebSocketManager.broadcast()
    """

    def __init__(
        self,
        websocket_manager
    ):

        self.websocket_manager = websocket_manager


    async def handle(
        self,
        event: DetectionEvent
    ):
        """
        处理DetectionEvent

        将事件转换为WebSocket消息
        """

        message = {

            # 事件类型
            "event_type":
                event.event_type,


            # 事件ID
            "event_id":
                event.event_id,


            # 时间
            "timestamp":
                event.timestamp,


            # 视频流
            "stream_name":
                event.stream_name,


            # AI插件
            "plugin_id":
                event.plugin_id,


            # AI结果
            "data":
                event.data,
        }


        logger.debug(
            "WebSocketConsumer handling event=%s stream=%s",
            event.event_id,
            event.stream_name
        )


        await self.websocket_manager.broadcast(
            event.stream_name,
            message
        )