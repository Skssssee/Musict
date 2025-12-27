# ======================================================
# utils/utils_system.py
# FIXED FOR py-tgcalls 2.2.x
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional, Dict

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ✅ CORRECT IMPORTS FOR py-tgcalls 2.2.x
from pytgcalls import PyTgCalls
from pytgcalls.types.stream import AudioPiped, AudioVideoPiped

from assistants.assistant_system import assistant
from config import COOKIE_URL, LOGGER_ID


# ======================================================
# LOGGER SETUP
# ======================================================

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/musicbot.log"),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger("MusicBot")


async def send_log(bot, text: str):
    if not LOGGER_ID:
        return
    try:
        await bot.send_message(LOGGER_ID, text)
    except Exception:
        pass


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
                    data = await resp.text()
                    os.makedirs("cookies", exist_ok=True)
                    with open(COOKIES_PATH, "w", encoding="utf-8") as f:
                        f.write(data)
                    LOGGER.info("YouTube cookies loaded")
    except Exception as e:
        LOGGER.error(f"Cookie load failed: {e}")


# ======================================================
# PYTGCALLS INIT
# ======================================================

call = PyTgCalls(assistant)


# ======================================================
# YT-DLP STREAM (NO DOWNLOAD)
# ======================================================

def _yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }


async def get_audio_stream(query: str) -> Optional[str]:
    with yt_dlp.YoutubeDL(_yt_opts()) as ydl:
        info = ydl.extract_info(query, download=False)
        return info["url"]


async def get_video_stream(query: str) -> Optional[str]:
    opts = _yt_opts()
    opts["format"] = "bestvideo[height<=360]+bestaudio/best"

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info["url"]


# ======================================================
# VOICE CHAT CONTROLS
# ======================================================

async def play_audio(chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        AudioPiped(stream_url)
    )


async def play_video(chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        AudioVideoPiped(stream_url)
    )


async def stop_stream(chat_id: int):
    try:
        await call.leave_group_call(chat_id)
    except Exception:
        pass


# ======================================================
# SIMPLE CACHE
# ======================================================

STREAM_CACHE: Dict[str, str] = {}

def get_cached(query: str):
    return STREAM_CACHE.get(query)

def set_cache(query: str, url: str):
    STREAM_CACHE[query] = url


# ======================================================
# PLAYER UI
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
            ]
        ]
    )


def now_playing_text(title, duration, user):
    return (
        f"🎶 **Now Playing**\n\n"
        f"**Title:** {title}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {user.mention}"
    )


# ======================================================
# INIT
# ======================================================

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils initialized successfully")
