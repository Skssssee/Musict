# ======================================================
# app.py
# MAIN ENTRY POINT
# ======================================================

import asyncio
from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN

# ---- ASSISTANT (USER ACCOUNT) ----
from assistants.assistant_system import start_assistant

# ---- UTILS ----
from utils.utils_system import (
    LOGGER,
    init_utils,
    get_call,   # ✅ SAFE PyTgCalls getter
)

# ---- BOT CLIENT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ---- LOAD PLUGINS (AUTO LOAD CORE) ----
import plugins.plugins_system   # ❗ REQUIRED


async def main():
    # 1️⃣ Init utils (logs, cache, cookies)
    await init_utils()

    # 2️⃣ Start assistant (user account)
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # 3️⃣ Init & start PyTgCalls
    LOGGER.info("Starting PyTgCalls...")
    call = get_call()          # ✅ IMPORTANT
    await call.start()

    # 4️⃣ Start bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # 5️⃣ Idle
    await bot.idle()


if __name__ == "__main__":
    bot.run(main())
