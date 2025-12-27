
# ======================================================
# utils/utils_system.py
# ALL SHARED UTILS (NO COMMANDS HERE)
# ======================================================

import os
import time
import logging
from collections import defaultdict, deque
from typing import Dict, Deque, Optional

import yt_dlp
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import COOKIE_URL
from core.core_system import is_logger_enabled, get_logger_chat


# ======================================================
# LOGGER (FILE + LOGGER GC)
# ======================================================

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGER = logging.getLogger("MusicBot")
LOGGER.setLevel(logging.INFO)

file_handler = logging.FileHandler("logs/musicbot.log")
file_handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
)

LOGGER.addHandler(file_handler)


async def send_log(bot, text: str):
    """
    Send log message to LOGGER GC (if enabled)
    """
    if not is_logger_enabled():
        return

    chat_id = get_logger_chat()
    if not chat_id:
        return

    try:
        await bot.send_message(chat_id, f"📜 **LOG**\n{text}")
    except Exception as e:
        LOGGER.error(f"Failed to send log: {e}")


# ======================================================
# QUEUE SYSTEM (IN-MEMORY)
# ======================================================

QUEUE: Dict[int, Deque[dict]] = defaultdict(deque)
NOW_PLAYING: Dict[int, dict] = {}


def add_to_queue(chat_id: int, track: dict):
    QUEUE[chat_id].append(track)


def get_next(chat_id: int) -> Optional[dict]:
    if QUEUE[chat_id]:
        return QUEUE[chat_id].popleft()
    return None


def clear_queue(chat_id: int):
    QUEUE[chat_id].clear()
    NOW_PLAYING.pop(chat_id, None)


def get_queue(chat_id: int):
    return list(QUEUE[chat_id])


# ======================================================
# TIME + PROGRESS BAR
# ======================================================

def format_time(seconds: int) -> str:
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def progress_bar(elapsed: int, total: int, size: int = 12) -> str:
    if total <= 0:
        return "━" * size
    filled = int(size * elapsed / total)
    return "▰" * filled + "▱" * (size - filled)


# ======================================================
# INLINE PLAYER UI
# ======================================================

def player_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏭ Skip", callback_data="skip"),
                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
            ],
            [
                InlineKeyboardButton("📃 Queue", callback_data="queue"),
                InlineKeyboardButton("❌ Close", callback_data="close"),
            ],
        ]
    )


def now_playing_text(track: dict, user) -> str:
    return (
        f"🎶 **Now Playing**\n\n"
        f"**Title:** {track['title']}\n"
        f"**Duration:** {format_time(track['duration'])}\n"
        f"**Requested by:** {user.mention}"
    )


# ======================================================
# COOKIES HANDLING (YT BLOCK FIX)
# ======================================================

COOKIES_FILE = "cookies/cookies.txt"


def ensure_cookies():
    """
    If COOKIE_URL is given, yt-dlp will auto use cookies.txt
    """
    if COOKIE_URL and os.path.exists(COOKIES_FILE):
        return COOKIES_FILE
    return None


# ======================================================
# YOUTUBE STREAM FETCH (NO DOWNLOAD)
# ======================================================

YDL_OPTS = {
    "quiet": True,
    "no_warnings": True,
    "noplaylist": True,
    "format": "bestaudio/best",
}


def fetch_youtube(query: str) -> dict:
    """
    Returns stream URL + metadata (NO DOWNLOAD)
    """
    cookies = ensure_cookies()
    if cookies:
        YDL_OPTS["cookiefile"] = cookies

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(query, download=False)

        return {
            "title": info.get("title"),
            "url": info["url"],
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail"),
        }


# ======================================================
# STREAM HELPERS (USED BY PyTgCalls)
# ======================================================

async def get_audio_stream(query: str) -> dict:
    return fetch_youtube(query)


async def get_video_stream(query: str) -> dict:
    YDL_OPTS["format"] = "bestvideo[height<=360]+bestaudio/best"
    return fetch_youtube(query)


# ======================================================
# WHY THIS FILE EXISTS (SUMMARY)
# ======================================================
"""
utils_system.py kya karta hai?

✅ Queue management
✅ Progress bar + time formatting
✅ Inline buttons UI
✅ YouTube direct stream (NO download → low storage)
✅ Cookies support (YT block bypass)
✅ Logger (file + logger GC)

❌ Commands nahi
❌ Bot decorators nahi
❌ Assistant login nahi
"""
