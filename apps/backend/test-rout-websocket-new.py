python - <<'PY'
from app.routers import websocket

for r in websocket.router.routes:
    print(type(r).__name__, getattr(r,"path",None))
PY