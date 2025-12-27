
# ======================================================
# utils/utils_system.py
# ALL UTILS MERGED IN ONE FILE
# ======================================================

import os
import time
import logging
import asyncio
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

from assistants.assistant_system import assistant
from config import COOKIE_URL, LOGGER_ID


# ======================================================
# LOGGER SYSTEM (utils/logger.py + logs_system.py)
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
    """
    Send log message to LOGGER_ID (if provided)
    """
    if not LOGGER_ID:
        return
    try:
        await bot.send_message(LOGGER_ID, text)
    except Exception:
        pass


# ======================================================
# SAFE ERROR HANDLER (utils/errors.py)
# ======================================================

async def safe_reply(message, text: str):
    """
    Safe reply wrapper to avoid crashes
    """
    try:
        await message.reply(text)
    except Exception:
        pass


# ======================================================
# COOKIE SYSTEM (utils/cookies.py)
# ======================================================

COOKIES_PATH = "cookies/cookies.txt"

async def load_cookies():
    """
    Load cookies from COOKIE_URL (batbin/gist)
    Saves to cookies/cookies.txt
    """
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
                    LOGGER.info("YouTube cookies loaded successfully")
    except Exception as e:
        LOGGER.error(f"Cookie load failed: {e}")


# ======================================================
# PYTGCALLS INIT (utils/utils.py)
# ======================================================

call = PyTgCalls(assistant)


# ======================================================
# YOUTUBE STREAM HELPERS (utils/youtube.py)
# ======================================================

def _yt_opts():
    """
    Base yt-dlp options (NO DOWNLOAD)
    """
    opts = {
        "quiet": True,
        "no_warnings": True,
        "nocheckcertificate": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }
    return opts


async def get_audio_stream(query: str) -> Optional[str]:
    """
    Returns direct audio stream URL
    """
    ydl_opts = _yt_opts()
    ydl_opts["format"] = "bestaudio/best"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


async def get_video_stream(query: str) -> Optional[str]:
    """
    Returns direct video stream URL (<=360p)
    """
    ydl_opts = _yt_opts()
    ydl_opts["format"] = "bestvideo[height<=360]+bestaudio/best"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


# ======================================================
# VOICE CHAT HELPERS (utils/vc.py)
# ======================================================

async def play_audio(chat_id: int, stream_url: str):
    """
    Join VC & play audio
    """
    await call.join_group_call(
        chat_id,
        AudioPiped(stream_url, HighQualityAudio()),
    )


async def play_video(chat_id: int, stream_url: str):
    """
    Join VC & play video (360p)
    """
    await call.join_group_call(
        chat_id,
        AudioVideoPiped(
            stream_url,
            HighQualityAudio(),
            MediumQualityVideo()
        ),
    )


async def stop_stream(chat_id: int):
    """
    Stop VC stream
    """
    try:
        await call.leave_group_call(chat_id)
    except Exception:
        pass


# ======================================================
# CACHE SYSTEM (utils/cache.py)
# ======================================================
# Same song repeat ho → instant play

STREAM_CACHE: Dict[str, str] = {}

def get_cached(query: str) -> Optional[str]:
    return STREAM_CACHE.get(query)

def set_cache(query: str, stream_url: str):
    STREAM_CACHE[query] = stream_url


# ======================================================
# PLAYER UI (utils/player_ui.py)
# ======================================================

def player_buttons():
    """
    Inline buttons for player
    """
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


def now_playing_text(title: str, duration: str, user):
    """
    Now playing message formatter
    """
    return (
        f"🎶 **Now Playing**\n\n"
        f"**Title:** {title}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {user.mention}"
    )


# ======================================================
# UTILS INIT HOOK
# ======================================================

async def init_utils():
    """
    Call once on startup
    """
    await load_cookies()
    LOGGER.info("Utils system initialized")
