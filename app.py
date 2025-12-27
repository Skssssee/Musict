# app.py

import asyncio
from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN
from assistants.assistant_system import assistant, start_assistant
from utils.utils_system import LOGGER, init_utils, get_call

# ---- BOT CLIENT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- LOAD PLUGINS (DO NOT REMOVE) ----
import plugins.plugins_system


async def main():
    # Utils
    await init_utils()

    # Assistant start
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # 🔥 START PYTGCALLS PROPERLY (THIS WAS MISSING)
    call = get_call(assistant)
    await call.start()
    LOGGER.info("PyTgCalls started")

    # Start bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # Idle forever
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
