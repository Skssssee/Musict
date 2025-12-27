# ======================================================
# app.py
# MAIN ENTRY POINT (FIXED)
# ======================================================

import asyncio

from pyrogram import Client
from pyrogram.idle import idle

from config import API_ID, API_HASH, BOT_TOKEN

# ---- ASSISTANT (USER ACCOUNT) ----
from assistants.assistant_system import assistant, start_assistant

# ---- UTILS ----
from utils.utils_system import (
    LOGGER,
    init_utils,
    get_call,
)

# ---- BOT CLIENT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- LOAD PLUGINS (AUTO LOAD COMMANDS) ----
import plugins.plugins_system   # ❗ DO NOT REMOVE


async def main():
    # 1️⃣ Init utils (cookies, logger)
    await init_utils()

    # 2️⃣ Start assistant (user account)
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # 3️⃣ Init PyTgCalls with assistant
    LOGGER.info("Starting PyTgCalls...")
    call = get_call(assistant)
    await call.start()

    # 4️⃣ Start bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # 5️⃣ Idle
    await idle()

    # 6️⃣ Shutdown (optional safety)
    await bot.stop()
    await assistant.stop()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
