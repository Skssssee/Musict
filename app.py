# ======================================================
# app.py
# MAIN ENTRY POINT (PYROGRAM 2.x FIXED)
# ======================================================

import asyncio
from pyrogram import Client, idle

from config import API_ID, API_HASH, BOT_TOKEN

# ---- ASSISTANT ----
from assistants.assistant_system import assistant, start_assistant

# ---- UTILS ----
from utils.utils_system import LOGGER, init_utils, get_call

# ---- BOT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- LOAD PLUGINS ----
import plugins.plugins_system


async def main():
    # Utils init
    await init_utils()

    # Assistant start
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # PyTgCalls init
    LOGGER.info("Starting PyTgCalls...")
    call = get_call(assistant)
    await call.start()

    # Bot start
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # Idle (Pyrogram 2.x)
    await idle()

    # Shutdown
    await bot.stop()
    await assistant.stop()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
