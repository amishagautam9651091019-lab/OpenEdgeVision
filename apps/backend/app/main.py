from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.health import router as health_router
from app.routers.streams import router as streams_router


app = FastAPI(
    title="OpenEdge Vision API",
    version=settings.version,
    description="OpenEdge Vision Edge AI Platform",
)


# 开发阶段允许 Vue 前端跨域访问 FastAPI。
# 当前兼容：
# - localhost
# - 127.0.0.1
# - Ubuntu 虚拟机 IP：192.168.111.128
# - Vite 可能使用的任意开发端口
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=(
        r"^http://("
        r"localhost|"
        r"127\.0\.0\.1|"
        r"192\.168\.111\.128"
        r"):\d+$"
    ),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 注册健康检查接口
app.include_router(health_router)

# 注册视频流接口
app.include_router(streams_router)


@app.get("/", tags=["Root"])
def root() -> dict[str, str]:
    """Platform root endpoint."""

    return {
        "name": "OpenEdge Vision",
        "version": settings.version,
        "status": "running",
    }