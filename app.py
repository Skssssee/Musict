from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

from assistants.assistant_system import assistant, start_assistant
from utils.utils import call
from utils.logs_system import LOGGER

# load combined plugins
import plugins.plugins_system

bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

async def main():
    LOGGER.info("Starting assistant...")
    await start_assistant()

    LOGGER.info("Starting PyTgCalls...")
    await call.start()

    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("MusicBot started successfully")
    await bot.idle()

bot.run(main())
