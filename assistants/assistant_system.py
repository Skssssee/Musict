
# assistants/assistant_system.py

from pyrogram import Client
from pyrogram.errors import RPCError

from config import API_ID, API_HASH, STRING_SESSION
from utils.logger import LOGGER   # ✅ SAFE IMPORT


assistant = Client(
    name="assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True,
)


async def start_assistant():
    try:
        await assistant.start()
        me = await assistant.get_me()
        LOGGER.info(
            f"Assistant logged in as {me.first_name} (@{me.username}) | ID: {me.id}"
        )
    except RPCError as e:
        LOGGER.error(f"Assistant start failed: {e}")
        raise SystemExit("Assistant could not start")


async def stop_assistant():
    try:
        await assistant.stop()
        LOGGER.info("Assistant stopped successfully")
    except Exception as e:
        LOGGER.error(f"Assistant stop error: {e}")
