import websocket
import json


url = "ws://127.0.0.1:8000/ws/streams/drone01"


print("connecting:", url)


ws = websocket.create_connection(
    url
)


print("WebSocket connected")


try:

    while True:

        msg = ws.recv()

        data = json.loads(msg)

        print(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            )
        )


except KeyboardInterrupt:

    print("closed")

finally:

    ws.close()