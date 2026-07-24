from typing import Callable, Dict, List


class EventBus:
    """
    简单事件总线

    Publisher:
        发布事件

    Subscriber:
        订阅事件
    """

    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}


    def subscribe(
        self,
        event_type: str,
        handler: Callable
    ):
        """
        注册事件消费者
        """

        if event_type not in self.handlers:
            self.handlers[event_type] = []

        self.handlers[event_type].append(handler)


    async def publish(self, event):
        """
        发布事件
        """

        handlers = self.handlers.get(
            event.event_type,
            []
        )

        for handler in handlers:
            await handler(event)