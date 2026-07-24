import pytest

from app.events import EventRuntime


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
                "stream_name":stream_name,
                "data":data
            }
        )



@pytest.mark.asyncio
async def test_event_runtime_register_websocket_consumer():

    manager = MockWebSocketManager()


    runtime = EventRuntime(
        manager
    )


    event = {
        "event_type":"detection",
        "stream_name":"drone01",
        "plugin_id":"mock-detector",
        "data":{
            "confidence":0.9
        }
    }


    from app.events import DetectionEvent


    detection_event = DetectionEvent(
        **event
    )


    await runtime.get_bus().publish(
        detection_event
    )


    assert len(
        manager.messages
    ) == 1


    assert (
        manager.messages[0]
        ["stream_name"]
        ==
        "drone01"
    )