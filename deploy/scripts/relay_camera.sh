#!/usr/bin/env bash
set -euo pipefail
SOURCE_RTSP="${1:?Usage: ./relay_camera.sh <source-rtsp> [stream-name]}"
STREAM_NAME="${2:-park01}"
ffmpeg -rtsp_transport tcp -i "$SOURCE_RTSP" -c copy -f rtsp "rtsp://localhost:8554/${STREAM_NAME}"
