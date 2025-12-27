# app.py

import asyncio
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant

from config import API_ID, API_HASH, BOT_TOKEN, LOGGER_ID
from assistants.assistant_system import start_assistant, assistant
from utils.utils_system import LOGGER, init_utils

# 🔥 BOT CLIENT
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="bot_session"     # 🔥 IMPORTANT
)

# LOAD PLUGINS
import plugins.plugins_system   # DO NOT REMOVE


async def main():
    # Utils
    await init_utils()

    # Assistant
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # OPTIONAL: auto-join logger group
    if LOGGER_ID:
        try:
            await assistant.join_chat(LOGGER_ID)
            await assistant.send_message(
                LOGGER_ID,
                "✅ Assistant active & stable"
            )
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            LOGGER.warning(f"Assistant join skipped: {e}")

    # Bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # KEEP ALIVE
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
