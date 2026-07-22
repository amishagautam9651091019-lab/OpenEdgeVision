import time

import cv2

from app.video.frame_provider import frame_provider


STREAM_NAME = "drone01"

# 按你的 MediaMTX 实际地址修改。
STREAM_URL = "rtsp://127.0.0.1:8554/drone01"


def main() -> None:
    frame_provider.add_stream(
        stream_name=STREAM_NAME,
        stream_url=STREAM_URL,
    )

    print("Waiting for RTSP frame...")

    snapshot = None

    for _ in range(50):
        snapshot = frame_provider.get_latest_frame(
            STREAM_NAME
        )

        if snapshot is not None:
            break

        print(
            frame_provider.get_stream_status(
                STREAM_NAME
            )
        )

        time.sleep(0.2)

    if snapshot is None:
        raise RuntimeError(
            "No video frame received within 10 seconds"
        )

    print("Frame received successfully")
    print(f"frame_id: {snapshot.frame_id}")
    print(f"shape: {snapshot.frame.shape}")
    print(f"width: {snapshot.width}")
    print(f"height: {snapshot.height}")
    print(f"timestamp: {snapshot.timestamp}")

    output_path = "/tmp/openedge_day7_frame.jpg"

    success = cv2.imwrite(
        output_path,
        snapshot.frame,
    )

    if not success:
        raise RuntimeError(
            f"Unable to save test frame: {output_path}"
        )

    print(f"Saved test frame: {output_path}")

    frame_provider.shutdown()


if __name__ == "__main__":
    main()