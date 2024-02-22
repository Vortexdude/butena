class Config:
    PORT: int = 8000
    HOST: str = '0.0.0.0'
    ENV: str = 'dev'
    WORKER_COUNT: int = 1
    RELOAD: bool = True
    MONGO_DB_HOST = '127.0.0.1'
    MONGO_DB_PORT = 27017
    DATABASE = 'butena'
    JWT_SECRET_KEY = "nothing_special"
    JWT_REFRESH_SECRET_KEY = "very_special"
    ALGORITHM = "HS256"
    TEMP_DIR = "/tmp/git"
    BUCKET_NAME = 'butena-public'
    ZONE = 'ap-south-1'
