python - <<'PY'
from app.main import app

for path, method in app.openapi()["paths"].items():
    print(method.keys(), path)
PY