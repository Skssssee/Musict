# ======================================================
# config.py
# MAIN CONFIGURATION FILE
# ======================================================

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


# ======================================================
# ENV HELPER
# ======================================================

def get_env(name, cast=str, default=None):
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required env var: {name}")
    try:
        return cast(value)
    except Exception:
        raise RuntimeError(f"Invalid value for env var: {name}")


# ======================================================
# TELEGRAM CORE CONFIG
# ======================================================

API_ID = get_env("API_ID", int)
API_HASH = get_env("API_HASH")
BOT_TOKEN = get_env("BOT_TOKEN")

# Assistant (user account)
STRING_SESSION = get_env("STRING_SESSION")

OWNER_ID = get_env("OWNER_ID", int)

# Logger group (optional)
LOGGER_ID = int(os.getenv("LOGGER_ID")) if os.getenv("LOGGER_ID") else None


# ======================================================
# DATABASE (MONGODB ATLAS)
# ======================================================
# DATABASE_NAME is OPTIONAL for Atlas

MONGO_DB_URI = get_env("MONGO_DB_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")  # optional


# ======================================================
# COOKIES / YT-DLP
# ======================================================

COOKIE_URL = os.getenv("COOKIE_URL")  # optional


# ======================================================
# OPTIONAL / SAFE DEFAULTS
# ======================================================

DEBUG = os.getenv("DEBUG", "False").lower() == "true"


# ======================================================
# VALIDATION LOG
# ======================================================

print("✅ Config loaded successfully")
print(f"• API_ID: {API_ID}")
print(f"• OWNER_ID: {OWNER_ID}")
print(f"• LOGGER_ID: {LOGGER_ID}")
print(f"• MongoDB URI set: {bool(MONGO_DB_URI)}")
print(f"• Database Name: {DATABASE_NAME}")
