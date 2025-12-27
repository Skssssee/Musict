# utils/utils_system.py

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from config import COOKIE_URL, LOGGER_ID

# ======================================================
# LOGGER
# ======================================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("logs/musicbot.log"),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger("MusicBot")

# ======================================================
# PYTGCALLS (assistant injected later)
# ======================================================

call: PyTgCalls | None = None

def init_pytgcalls(assistant_client):
    global call
    call = PyTgCalls(assistant_client)

# ======================================================
# COOKIE SYSTEM
# ======================================================

COOKIES_PATH = "cookies/cookies.txt"

async def load_cookies():
    if not COOKIE_URL:
        return
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COOKIE_URL) as resp:
                if resp.status == 200:
                    os.makedirs("cookies", exist_ok=True)
                    with open(COOKIES_PATH, "w", encoding="utf-8") as f:
                        f.write(await resp.text())
                    LOGGER.info("Cookies loaded")
    except Exception as e:
        LOGGER.error(f"Cookie error: {e}")

# ======================================================
# YOUTUBE STREAM
# ======================================================

def _yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }

async def get_audio_stream(query: str) -> Optional[str]:
    with yt_dlp.YoutubeDL({**_yt_opts(), "format": "bestaudio"}) as ydl:
        return ydl.extract_info(query, download=False).get("url")

async def get_video_stream(query: str) -> Optional[str]:
    with yt_dlp.YoutubeDL({**_yt_opts(), "format": "best[height<=360]"}) as ydl:
        return ydl.extract_info(query, download=False).get("url")

# ======================================================
# VC CONTROL
# ======================================================

async def play_audio(chat_id: int, url: str):
    await call.join_group_call(chat_id, url, stream_type="audio")

async def play_video(chat_id: int, url: str):
    await call.join_group_call(chat_id, url, stream_type="video")

async def stop_stream(chat_id: int):
    await call.leave_group_call(chat_id)

# ======================================================
# UI
# ======================================================

def player_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏭ Skip", callback_data="skip"),
                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
            ],
            [InlineKeyboardButton("❌ Close", callback_data="close")]
        ]
    )

# ======================================================
# INIT
# ======================================================

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils ready")
