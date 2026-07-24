import logging

from app.events import EventBus
from app.events.consumers import WebSocketConsumer


logger = logging.getLogger(__name__)


class EventRuntime:
    """
    OpenEdgeVision事件运行时


    管理：

    1. EventBus生命周期

    2. Consumer注册


    当前Consumer:

    - WebSocketConsumer

    后续:

    - StorageConsumer

    - AlarmConsumer

    - CloudSyncConsumer

    """

    def __init__(
        self,
        websocket_manager
    ):

        self.bus = EventBus()


        self.websocket_consumer = (
            WebSocketConsumer(
                websocket_manager
            )
        )


        self.register_consumers()


        logger.info(
            "EventRuntime initialized"
        )


    def register_consumers(self):
        """
        注册事件消费者
        """

        self.bus.subscribe(
            "detection",
            self.websocket_consumer.handle
        )


    def get_bus(self):
        """
        获取EventBus实例
        """

        return self.bus