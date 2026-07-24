"""
EventBus 单元测试

验证：
1. Event创建
2. 单消费者订阅
3. 事件发布
4. 多消费者广播
5. 不同event_type隔离
"""

import pytest

from app.events import (
    EventBus,
    DetectionEvent,
)


@pytest.mark.asyncio
async def test_event_bus_publish_subscribe():
    """
    测试：
    一个事件发布，一个消费者接收
    """

    bus = EventBus()

    received_events = []


    async def detection_handler(event):

        received_events.append(event)


    # 注册消费者
    bus.subscribe(
        "detection",
        detection_handler
    )


    # 创建事件
    event = DetectionEvent(
        event_type="detection",
        stream_name="drone01",
        plugin_id="mock-detector",
        data={
            "class_name": "mock-target",
            "confidence": 0.95
        }
    )


    # 发布事件
    await bus.publish(event)


    # 验证
    assert len(received_events) == 1

    received = received_events[0]


    assert received.event_type == "detection"

    assert received.stream_name == "drone01"

    assert received.plugin_id == "mock-detector"

    assert received.data["class_name"] == "mock-target"

    assert received.data["confidence"] == 0.95



@pytest.mark.asyncio
async def test_event_bus_multiple_handlers():
    """
    测试：
    一个事件发送给多个消费者

    模拟：

    EventBus

       |
       +---- WebSocket Consumer

       |
       +---- Storage Consumer
    """

    bus = EventBus()

    received = []


    async def websocket_handler(event):

        received.append(
            "websocket"
        )


    async def storage_handler(event):

        received.append(
            "storage"
        )


    # 两个消费者订阅同一个事件

    bus.subscribe(
        "detection",
        websocket_handler
    )


    bus.subscribe(
        "detection",
        storage_handler
    )


    event = DetectionEvent(
        event_type="detection",
        stream_name="drone01",
        plugin_id="mock-detector",
        data={}
    )


    await bus.publish(event)


    assert len(received) == 2

    assert "websocket" in received

    assert "storage" in received



@pytest.mark.asyncio
async def test_event_bus_event_type_isolation():
    """
    测试：
    不同event_type不会互相触发
    """

    bus = EventBus()

    received = []


    async def detection_handler(event):

        received.append(event.event_type)


    async def alarm_handler(event):

        received.append(event.event_type)


    bus.subscribe(
        "detection",
        detection_handler
    )


    bus.subscribe(
        "alarm",
        alarm_handler
    )


    detection_event = DetectionEvent(
        event_type="detection",
        stream_name="drone01",
        plugin_id="mock-detector",
        data={}
    )


    alarm_event = DetectionEvent(
        event_type="alarm",
        stream_name="drone01",
        plugin_id="system",
        data={}
    )


    await bus.publish(
        detection_event
    )


    await bus.publish(
        alarm_event
    )


    assert len(received) == 2

    assert "detection" in received

    assert "alarm" in received



@pytest.mark.asyncio
async def test_detection_event_auto_generate_fields():
    """
    测试：
    DetectionEvent自动生成：

    event_id
    timestamp
    """

    event = DetectionEvent(
        event_type="detection",
        stream_name="drone01",
        plugin_id="mock-detector",
        data={}
    )


    assert event.event_id is not None

    assert len(event.event_id) > 0

    assert event.timestamp > 0