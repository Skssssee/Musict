from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from assistants.assistant_system import start_assistant
from utils.utils_system import get_call
from utils.logger import LOGGER

bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

import plugins.plugins_system


async def main():
    LOGGER.info("Starting assistant...")
    await start_assistant()

    LOGGER.info("Starting PyTgCalls...")
    call = get_call()
    await call.start()

    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")
    await bot.idle()


if __name__ == "__main__":
    bot.run(main())
