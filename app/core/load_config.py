import os
from dotenv import load_dotenv


class EnvConfig:

    def __init__(self):
        load_dotenv(verbose=True)

    @staticmethod
    def _get_env(key, default):
        return os.getenv(key, default)

    @property
    def api_title(self) -> str:
        return self._get_env("API_TITLE", 'Butena')

    @property
    def description(self) -> str:
        return self._get_env("DESCRIPTION", 'FastAPI Starter Project')

    @property
    def doc_url(self) -> str:
        return self._get_env("DOC_URL", '/api/docs')

    @property
    def redoc_url(self) -> str:
        return self._get_env("REDOC_URL", '/api/redoc/')

    @property
    def api_port(self) -> int:
        return self._get_env("API_PORT", 8000)

    @property
    def api_host(self) -> str:
        return self._get_env("API_HOST", '0.0.0.0')

    @property
    def api_env(self) -> str:
        return self._get_env("API_ENV", 'dev')

    @property
    def api_version(self) -> float:
        return self._get_env("API_VERSION", 1.0)

    @property
    def worker_count(self) -> int:
        return self._get_env("WORKER_COUNT", 1)

    @property
    def server_reload(self) -> bool:
        return self._get_env("SERVER_RELOAD", False)

    @property
    def postgres_host(self) -> str:
        return self._get_env("POSTGRES_HOST", '127.0.0.1')

    @property
    def postgres_port(self) -> int:
        return self._get_env("POSTGRES_PORT", 5432)

    @property
    def postgres_database(self) -> str:
        return self._get_env("POSTGRES_DB", 'butena')

    @property
    def postgres_username(self) -> str:
        return self._get_env("POSTGRES_USER", 'butena')

    @property
    def postgres_password(self) -> str:
        return self._get_env("POSTGRES_PASSWORD", 'supersecret')

    @property
    def sqlalchemy_database_uri(self) -> str:
        POSTGRES = {
            "user": self.postgres_username,
            "pw": self.postgres_password,
            "host": self.postgres_host,
            "port": self.postgres_port,
            "db": self.postgres_database,
        }
        if not POSTGRES['user']:
            return self._get_env("SQLALCHEMY_DATABASE_URI", "sqlite:///data.db")
        return "postgresql+psycopg2://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES

    @property
    def jwt_secret_key(self) -> str:
        return self._get_env("JWT_SECRET_KEY", "secret")

    @property
    def jwt_refresh_secret_key(self) -> str:
        return self._get_env("JWT_REFRESH_SECRET_KEY", "supersecret")

    @property
    def algorthm(self) -> str:
        return self._get_env("ALGORITHM", "HS256")

    @property
    def temp_dir(self) -> str:
        return self._get_env("TEMP_DIR", "/tmp/git")

    @property
    def bucket_name(self) -> str:
        return self._get_env("BUCKET_NAME", "butena-public")

    @property
    def aws_bucket_zone(self) -> str:
        return self._get_env("BUCKET_ZONE", "ap-south-1")
