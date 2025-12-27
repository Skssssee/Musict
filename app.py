
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

# ---- BOT CLIENT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- LOAD COMMANDS ----
import plugins.plugins_system  # ❗ REQUIRED


async def main():
    # 1️⃣ Init utils
    await init_utils()

    # 2️⃣ Start assistant
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # 3️⃣ Start PyTgCalls
    LOGGER.info("Starting PyTgCalls...")
    call = get_call(assistant)
    await call.start()

    # 4️⃣ Start bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # 5️⃣ Idle
    await idle()

    # 6️⃣ Cleanup
    await bot.stop()
    await assistant.stop()


if __name__ == "__main__":
    asyncio.run(main())
