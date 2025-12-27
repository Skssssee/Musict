# ======================================================
# app.py
# MAIN ENTRY POINT (FIXED)
# ======================================================

from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# ---- ASSISTANT ----
from assistants.assistant_system import assistant, start_assistant

# ---- UTILS ----
from utils.utils_system import (
    LOGGER,
    init_utils,
    init_pytgcalls,
    call
)

# ---- BOT CLIENT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- LOAD PLUGINS (auto-load core & commands) ----
import plugins.plugins_system  # ❗ REQUIRED


async def main():
    # 1️⃣ Init utils (cookies, logs)
    await init_utils()

    # 2️⃣ Start assistant (USER ACCOUNT)
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # 3️⃣ Inject assistant into PyTgCalls
    init_pytgcalls(assistant)

    # 4️⃣ Start PyTgCalls (VC engine)
    LOGGER.info("Starting PyTgCalls...")
    await call.start()

    # 5️⃣ Start bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # 6️⃣ Idle
    await bot.idle()


if __name__ == "__main__":
    bot.run(main())
