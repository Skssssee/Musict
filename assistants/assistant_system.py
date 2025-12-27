# ======================================================
# assistants/assistant_system.py
# ASSISTANT (USER ACCOUNT) LOGIC
# ======================================================

from pyrogram import Client
from pyrogram.errors import RPCError

from config import API_ID, API_HASH, STRING_SESSION
from utils.utils_system import LOGGER


# ======================================================
# ASSISTANT CLIENT
# ======================================================
# ❗ IMPORTANT:
# - Ye BOT nahi hai
# - Ye ek REAL Telegram USER ACCOUNT hai
# - Voice chat join karne ka kaam sirf ye karta hai

assistant = Client(
    name="assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=STRING_SESSION,
    in_memory=True,   # disk par session file save nahi hogi
)


# ======================================================
# START ASSISTANT
# ======================================================
async def start_assistant():
    """
    Assistant (user account) ko start karta hai
    """
    try:
        await assistant.start()

        me = await assistant.get_me()
        LOGGER.info(
            f"Assistant logged in as "
            f"{me.first_name} (@{me.username}) | ID: {me.id}"
        )

    except RPCError as e:
        LOGGER.error(f"Assistant start failed: {e}")
        raise SystemExit("Assistant could not start")


# ======================================================
# STOP ASSISTANT
# ======================================================
async def stop_assistant():
    """
    Assistant ko safely stop karta hai
    """
    try:
        await assistant.stop()
        LOGGER.info("Assistant stopped successfully")
    except Exception as e:
        LOGGER.error(f"Assistant stop error: {e}")


# ======================================================
# ASSISTANT STATUS HELPERS
# ======================================================

async def get_assistant_id() -> int:
    """
    Assistant ka Telegram user ID return karta hai
    """
    me = await assistant.get_me()
    return me.id


async def is_assistant_alive() -> bool:
    """
    Check karta hai assistant connected hai ya nahi
    """
    try:
        await assistant.get_me()
        return True
    except Exception:
        return False


# ======================================================
# WHY THIS FILE IS IMPORTANT (SUMMARY)
# ======================================================
"""
assistant_system.py kya karta hai?

1️⃣ STRING_SESSION se user account login
2️⃣ Voice chat join karne ke liye ready rakhta hai
3️⃣ Bot se alag hota hai (BOT_TOKEN use nahi karta)
4️⃣ PyTgCalls isi assistant ke through kaam karta hai
5️⃣ Agar assistant down → VC stream impossible
"""
