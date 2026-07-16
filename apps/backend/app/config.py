from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "OpenEdge Vision Backend"
    version: str = "0.1.0"
    mediamtx_api: str = "http://127.0.0.1:9997"


settings = Settings()
