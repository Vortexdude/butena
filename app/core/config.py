from pydantic import BaseModel
from .load_config import EnvConfig

env_settings = EnvConfig()


class Settings(BaseModel):
    API_TITLE: str = env_settings.api_title
    DESCRIPTION: str = env_settings.description
    DOC_URL: str = env_settings.doc_url
    REDOC_URL: str = env_settings.redoc_url
    API_VERSION: int = env_settings.api_version
    API_ENV: str = env_settings.api_env
    API_HOST: str = env_settings.api_host
    API_PORT: int = int(env_settings.api_port)
    WORKER_COUNT: int = int(env_settings.worker_count)
    SERVER_RELOAD: bool = env_settings.server_reload
    POSTGRES_USER: str = env_settings.postgres_username
    POSTGRES_PASSWORD: str = env_settings.postgres_password
    POSTGRES_DB: str = env_settings.postgres_database
    POSTGRES_HOST: str = env_settings.postgres_host
    POSTGRES_PORT: int = env_settings.postgres_port
    JWT_SECRET_KEY: str = env_settings.jwt_secret_key
    JWT_REFRESH_SECRET_KEY: str = env_settings.jwt_refresh_secret_key
    ALGORITHM: str = env_settings.algorthm
    TEMP_DIR: str = env_settings.temp_dir
    BUCKET_NAME: str = env_settings.bucket_name
    BUCKET_ZONE: str = env_settings.aws_bucket_zone
    DATABASE_URI: str = env_settings.sqlalchemy_database_uri


settings = Settings()
