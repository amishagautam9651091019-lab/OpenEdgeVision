python - <<'PY'
from app.routers.health import router as health_router
from app.routers.plugins import router as plugins_router
from app.routers.streams import router as streams_router
from app.routers.frame_provider import router as frame_provider_router
from app.routers.pipeline import router as pipeline_router

routers = [
    ("health", health_router),
    ("plugins", plugins_router),
    ("streams", streams_router),
    ("frame_provider", frame_provider_router),
    ("pipeline", pipeline_router),
]

for name, r in routers:
    print("\n====", name, "====")
    print(type(r))
    print("routes:")
    for x in r.routes:
        print(" ", type(x).__name__, getattr(x, "path", None))
PY
