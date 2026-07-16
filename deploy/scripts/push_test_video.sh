#!/usr/bin/env bash
set -euo pipefail
INPUT_FILE="${1:?Usage: ./push_test_video.sh <video-file> [stream-name]}"
STREAM_NAME="${2:-drone01}"
ffmpeg -re -stream_loop -1 -i "$INPUT_FILE" -c copy -f rtsp "rtsp://localhost:8554/${STREAM_NAME}"
