from databases import DatabaseURL

from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "CoolProject"
VERSION = "1.0.0"
API_PREFIX = "/api"

SECRET_KEY = config("SECRET_KEY", cast=Secret)

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)


# CLOUD CREDS
AWS_SECRET_KEY_ID = config("AWS_SECRET_KEY_ID", cast=str)
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY", cast=str)
CLOUD_ENDPOINT_URL = config("CLOUD_ENDPOINT_URL", cast=str, default="https://storage.yandexcloud.net")

# CLOUD SETTINGS
BUCKET = config("BUCKET", cast=str, default="vlado")
CLOUD_LINK_LIFESPAN = config("CLOUD_LINK_LIFESPAN_SECONDS", cast=int, default=7 * 24 * 60 * 60) # age in seconds NOTE: Max alowed 7 days

ACCESS_TOKEN_EXPIRE_MINUTES = config(
  "ACCESS_TOKEN_EXPIRE_MINUTES",
  cast=int,
  default=7 * 24 * 60 #one week
)
JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="vlado:auth")
JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")

DATABASE_URL = config(
  "DATABASE_URL",
  cast=DatabaseURL,
  default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
)