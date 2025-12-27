# ======================================================
# app.py
# MAIN ENTRY POINT
# ======================================================

import asyncio
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN

# ---- ASSISTANT ----
from assistants.assistant_system import start_assistant

# ---- UTILS ----
from utils.utils_system import call, LOGGER, init_utils

# ---- BOT CLIENT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- LOAD PLUGINS ----
import plugins.plugins_system   # REQUIRED


async def main():
    await init_utils()

    LOGGER.info("Starting assistant...")
    await start_assistant()

    LOGGER.info("Starting PyTgCalls...")
    await call.start()

    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # ✅ CORRECT IDLE
    await idle()


if __name__ == "__main__":
    bot.run(main())
