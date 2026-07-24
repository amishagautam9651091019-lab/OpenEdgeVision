import asyncio
import logging

from app.events import EventBus
from app.events.consumers import WebSocketConsumer


logger = logging.getLogger(__name__)


_current_runtime = None
_main_loop = None



class EventRuntime:
    """
    OpenEdgeVision事件运行时

    管理：

    1. EventBus生命周期

    2. Consumer注册

    当前Consumer:

    - WebSocketConsumer
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

        self.bus.subscribe(
            "detection",
            self.websocket_consumer.handle
        )



    def get_bus(self):

        return self.bus





def set_runtime(runtime):

    global _current_runtime

    _current_runtime = runtime





def get_event_bus():

    if _current_runtime is None:

        return None

    return _current_runtime.get_bus()





def set_loop(loop):

    global _main_loop

    _main_loop = loop





def get_loop():

    return _main_loop