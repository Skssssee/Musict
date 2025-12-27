# ======================================================
# utils/utils_system.py
# ALL CORE UTILS (YT-DLP + PYTGCALLS SAFE)
# ======================================================

import os
import logging
from typing import Optional, Dict

import yt_dlp
import aiohttp

from pytgcalls import PyTgCalls
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
# SEND LOG (plugins depend on this)
# ======================================================

async def send_log(bot, text: str):
    try:
        from config import LOGGER_ID
        if LOGGER_ID:
            await bot.send_message(LOGGER_ID, text)
    except Exception:
        pass


# ======================================================
# PYTGCALLS SAFE SINGLETON
# ======================================================

_call: Optional[PyTgCalls] = None

def get_call() -> PyTgCalls:
    global _call
    if _call is None:
        from assistants.assistant_system import assistant
        _call = PyTgCalls(assistant)
    return _call


# ======================================================
# YT-DLP OPTIONS
# ======================================================

COOKIES_FILE = "cookies/cookies.txt"

def _ydl_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "cookiefile": COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
    }


# ======================================================
# STREAM FETCH (THIS WAS MISSING)
# ======================================================

async def get_audio_stream(query: str) -> Optional[str]:
    opts = _ydl_opts()
    opts["format"] = "bestaudio/best"

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


async def get_video_stream(query: str) -> Optional[str]:
    opts = _ydl_opts()
    opts["format"] = "bestvideo[height<=360]+bestaudio/best"

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


# ======================================================
# CACHE (fast repeat play)
# ======================================================

STREAM_CACHE: Dict[str, str] = {}

def get_cached(query: str) -> Optional[str]:
    return STREAM_CACHE.get(query)

def set_cache(query: str, url: str):
    STREAM_CACHE[query] = url


# ======================================================
# PLAYER BUTTONS
# ======================================================

def player_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                InlineKeyboardButton("▶ Resume", callback_data="resume"),
            ],
            [
                InlineKeyboardButton("⏭ Skip", callback_data="skip"),
                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
            ],
            [
                InlineKeyboardButton("❌ Close", callback_data="close"),
            ],
        ]
    )


# ======================================================
# INIT
# ======================================================

async def init_utils():
    LOGGER.info("Utils initialized successfully")
