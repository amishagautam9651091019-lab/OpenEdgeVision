import pytest

from app.events import DetectionEvent
from app.events.consumers import WebSocketConsumer


class MockWebSocketManager:

    def __init__(self):
        self.messages = []


    async def broadcast(
        self,
        stream_name,
        data
    ):

        self.messages.append(
            {
                "stream_name": stream_name,
                "data": data
            }
        )



@pytest.mark.asyncio
async def test_websocket_consumer_handle_event():

    manager = MockWebSocketManager()


    consumer = WebSocketConsumer(
        manager
    )


    event = DetectionEvent(
        event_type="detection",
        stream_name="drone01",
        plugin_id="mock-detector",
        data={
            "confidence":0.9
        }
    )


    await consumer.handle(event)


    assert len(manager.messages) == 1


    msg = manager.messages[0]


    assert msg["stream_name"] == "drone01"

    assert msg["data"]["plugin_id"] == "mock-detector"

    assert msg["data"]["data"]["confidence"] == 0.9