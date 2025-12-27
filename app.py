# ======================================================
# app.py  (FINAL – STABLE, NO PEER ERROR)
# ======================================================

import asyncio
from pyrogram import Client

from config import API_ID, API_HASH, BOT_TOKEN
from assistants.assistant_system import start_assistant
from utils.utils_system import LOGGER, init_utils

# ------------------------------------------------------
# BOT CLIENT
# ------------------------------------------------------
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ------------------------------------------------------
# LOAD PLUGINS (VERY IMPORTANT)
# ------------------------------------------------------
import plugins.plugins_system  # ❗ DO NOT REMOVE


# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
async def main():
    # 1️⃣ Init utils (cookies, logger)
    await init_utils()

    # 2️⃣ Start assistant (already added manually in group)
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # 3️⃣ Start bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # 4️⃣ Idle forever
    await asyncio.Event().wait()


# ------------------------------------------------------
# RUN
# ------------------------------------------------------
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
