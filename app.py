# ======================================================
# app.py  (FINAL – STABLE)
# ======================================================

import asyncio
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant

from config import API_ID, API_HASH, BOT_TOKEN, LOGGER_ID
from assistants.assistant_system import start_assistant, assistant
from utils.utils_system import LOGGER, init_utils

# ---- BOT CLIENT ----
bot = Client(
    "musicbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---- LOAD PLUGINS ----
import plugins.plugins_system   # DO NOT REMOVE


async def main():
    # 1️⃣ Utils
    await init_utils()

    # 2️⃣ Assistant
    LOGGER.info("Starting assistant...")
    await start_assistant()

    # 3️⃣ Auto-join logger group (FIX PEER ID INVALID)
    if LOGGER_ID:
        try:
            await assistant.join_chat(LOGGER_ID)
            await assistant.send_message(
                LOGGER_ID,
                "✅ Assistant joined group automatically"
            )
        except UserAlreadyParticipant:
            pass
        except Exception as e:
            LOGGER.warning(f"Assistant join failed: {e}")

    # 4️⃣ Start bot
    LOGGER.info("Starting bot...")
    await bot.start()

    LOGGER.info("🎵 MusicBot started successfully")

    # 5️⃣ Idle
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
