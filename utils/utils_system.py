# ======================================================
# utils/utils_system.py
# FIXED + CLEAN (NO CIRCULAR IMPORT)
# ======================================================

import os
import logging
from typing import Optional, Dict

import aiohttp
import yt_dlp

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import (
    HighQualityAudio,
    MediumQualityVideo,
)

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


async def send_log(bot, text: str):
    if not LOGGER_ID:
        return
    try:
        await bot.send_message(LOGGER_ID, text)
    except Exception:
        pass


# ======================================================
# COOKIES
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
                    LOGGER.info("YouTube cookies loaded")
    except Exception as e:
        LOGGER.error(f"Cookie load failed: {e}")


# ======================================================
# PYTGCALLS SINGLETON (IMPORTANT)
# ======================================================

_call: Optional[PyTgCalls] = None


def get_call(assistant):
    """
    Create PyTgCalls instance ONCE using assistant
    """
    global _call
    if _call is None:
        _call = PyTgCalls(assistant)
    return _call


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
    opts = _yt_opts()
    opts["format"] = "bestaudio/best"
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


async def get_video_stream(query: str) -> Optional[str]:
    opts = _yt_opts()
    opts["format"] = "bestvideo[height<=360]+bestaudio/best"
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


# ======================================================
# VOICE CHAT CONTROLS
# ======================================================

async def play_audio(call: PyTgCalls, chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        AudioPiped(stream_url, HighQualityAudio()),
    )


async def play_video(call: PyTgCalls, chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        AudioVideoPiped(
            stream_url,
            HighQualityAudio(),
            MediumQualityVideo()
        ),
    )


async def stop_stream(call: PyTgCalls, chat_id: int):
    try:
        await call.leave_group_call(chat_id)
    except Exception:
        pass


# ======================================================
# CACHE (OPTIONAL)
# ======================================================

STREAM_CACHE: Dict[str, str] = {}


def get_cached(query: str) -> Optional[str]:
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
            ],
        ]
    )


def now_playing_text(title: str, duration: str, user):
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
    LOGGER.info("Utils initialized")
