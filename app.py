# ======================================================
# app.py
# MAIN ENTRY POINT (FIXED)
# ======================================================

import asyncio
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN

# ASSISTANT
from assistants.assistant_system import assistant, start_assistant

# UTILS
from utils.utils_system import LOGGER, init_utils, get_call

# BOT
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# LOAD PLUGINS
import plugins.plugins_system


async def main():
    await init_utils()

    LOGGER.info("Starting assistant...")
    await start_assistant()

    LOGGER.info("Starting PyTgCalls...")
    call = get_call(assistant)
    await call.start()

    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    await idle()

    await bot.stop()
    await assistant.stop()


if __name__ == "__main__":
    asyncio.run(main())
