from app.services.websocket_manager import WebSocketManager
from app.events import EventRuntime


websocket_manager = WebSocketManager()


event_runtime = EventRuntime(
    websocket_manager
)