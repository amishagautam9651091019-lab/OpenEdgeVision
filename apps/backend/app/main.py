from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from app.config import settings


from app.routers.health import router as health_router
from app.routers.plugins import router as plugins_router
from app.routers.streams import router as streams_router
from app.routers.frame_provider import (
    router as frame_provider_router,
)
from app.routers.pipeline import ( 
    router as pipeline_router,
)

from app.plugins import register_builtin_plugins


from app.core.stream_config import DEFAULT_STREAMS

from app.services.frame_provider_service import (
    frame_provider_service,
)

from app.routers import results

from app.routers import websocket

from app.routers.websocket import router as websocket_router


logging.basicConfig(
    level=logging.INFO
)


logger = logging.getLogger(__name__)



@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    logger.info(
        "Starting OpenEdge Vision backend"
    )


    #
    # Day6 Plugin Framework
    #
    register_builtin_plugins()


    #
    # Day7 FrameProvider
    #
    frame_provider_service.initialize(
        DEFAULT_STREAMS
    )


    yield


    logger.info(
        "Stopping OpenEdge Vision backend"
    )


    frame_provider_service.shutdown()



app = FastAPI(
    title="OpenEdge Vision API",
    version=settings.version,
    description="OpenEdge Vision Edge AI Platform",
    lifespan=lifespan,
)



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



#
# Existing APIs
#
app.include_router(
        results.router
)


app.include_router(
    health_router
)


app.include_router(
    streams_router
)


app.include_router(
    plugins_router
)



#
# Day7 New API
#
app.include_router(
    frame_provider_router
)

app.include_router(
        pipeline_router
)

app.include_router(
        websocket.router
)

print("DEBUG websocket routes:")
for r in websocket.router.routes:
    print(
       type(r).__name__,
       getattr(r,"path",None)
    )



@app.get("/")
def root():

    return {
        "name": "OpenEdge Vision",
        "version": settings.version,
        "status": "running",
    }
