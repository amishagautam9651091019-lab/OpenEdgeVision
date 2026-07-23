python - <<'PY'
from app.routers import websocket

print("module:", websocket)
print("router:", websocket.router)

for r in websocket.router.routes:
    print(type(r).__name__, getattr(r,"path",None))
PY