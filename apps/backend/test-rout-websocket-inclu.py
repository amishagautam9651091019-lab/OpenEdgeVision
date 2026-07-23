python - <<'PY'
from app.main import app

def print_routes(router, level=0):

    for r in router.routes:

        print(
            "  "*level,
            type(r).__name__,
            getattr(r,"path",None)
        )

        if hasattr(r,"routes"):
            print_routes(r, level+1)


print_routes(app)
PY