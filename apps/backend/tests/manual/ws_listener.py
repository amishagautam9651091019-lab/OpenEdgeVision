import asyncio
import websockets


async def listen():

    url = "ws://127.0.0.1:8000/ws/streams/drone01"

    print(
        f"Connecting {url}"
    )


    async with websockets.connect(url) as websocket:

        print(
            "WebSocket connected"
        )


        while True:

            message = await websocket.recv()

            print("\n========== EVENT ==========")

            print(message)

            print("===========================\n")



if __name__ == "__main__":

    asyncio.run(
        listen()
    )