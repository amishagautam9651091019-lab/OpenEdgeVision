python - <<'PY'
from app.main import app

for r in app.routes:
    print(type(r).__name__, getattr(r, "path", None))
PY