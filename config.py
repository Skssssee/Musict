# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_env(name, cast=str, default=None):
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    return cast(value)

API_ID = get_env("API_ID", int)
API_HASH = get_env("API_HASH")
BOT_TOKEN = get_env("BOT_TOKEN")

STRING_SESSION = get_env("STRING_SESSION")
OWNER_ID = get_env("OWNER_ID", int)

LOGGER_ID = int(os.getenv("LOG_GROUP_ID")) if os.getenv("LOG_GROUP_ID") else None
MONGO_DB_URI = get_env("MONGO_DB_URI")
DATABASE_NAME=getenv("DATABASE_NAME")
COOKIE_URL = os.getenv("COOKIE_URL")
