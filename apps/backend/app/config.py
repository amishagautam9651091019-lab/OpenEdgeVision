from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """OpenEdge Vision application settings."""

    app_name: str = "OpenEdge Vision Backend"
    version: str = "0.1.0"

    # 当前FastAPI运行在Ubuntu宿主机，MediaMTX端口映射到本机9997。
    mediamtx_api_url: str = "http://127.0.0.1:9997"

    # 外部API请求超时时间。
    mediamtx_timeout_seconds: float = 5.0

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()