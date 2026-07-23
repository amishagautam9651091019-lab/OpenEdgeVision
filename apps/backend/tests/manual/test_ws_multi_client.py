import websocket
import threading
import json
import time


STREAM = "drone01"

URL = f"ws://127.0.0.1:8000/ws/streams/{STREAM}"


def client(name):

    print(
        name,
        "connecting",
        URL
    )

    ws = websocket.create_connection(URL)

    print(
        name,
        "connected"
    )

    while True:

        try:

            msg = ws.recv()

            print(
                "\n",
                name,
                "received:"
            )

            print(msg)


        except Exception as e:

            print(
                name,
                "error",
                e
            )

            break



if __name__ == "__main__":


    t1 = threading.Thread(
        target=client,
        args=("client-1",)
    )


    t2 = threading.Thread(
        target=client,
        args=("client-2",)
    )


    t1.start()

    t2.start()


    while True:

        time.sleep(1)