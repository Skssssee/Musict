import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from assistants.assistant_system import assistant, start_assistant
from utils.utils_system import LOGGER, init_utils, get_call

bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workdir="bot_session"
)

import plugins.plugins_system

async def main():
    await init_utils()

    LOGGER.info("Starting assistant...")
    await start_assistant()

    call = get_call(assistant)
    await call.start()
    LOGGER.info("PyTgCalls started")

    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started – now listening!")

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
