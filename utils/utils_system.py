# ======================================================
# utils/utils_system.py
# COMPLETE & STABLE (PyTgCalls 2.x)
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality

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
    """Send logs to LOGGER_ID"""
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
            async with session.get(COOKIE_URL) as r:
                if r.status == 200:
                    os.makedirs("cookies", exist_ok=True)
                    with open(COOKIES_PATH, "w", encoding="utf-8") as f:
                        f.write(await r.text())
                    LOGGER.info("YouTube cookies loaded")
    except Exception as e:
        LOGGER.error(f"Cookie load failed: {e}")


# ======================================================
# PYTGCALLS FACTORY (NO CIRCULAR IMPORT)
# ======================================================

_call: PyTgCalls | None = None

def get_call(assistant) -> PyTgCalls:
    global _call
    if _call is None:
        _call = PyTgCalls(assistant)
    return _call


# ======================================================
# YT-DLP HELPERS (NO DOWNLOAD)
# ======================================================

def _yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }


async def get_audio_stream(url: str) -> str:
    opts = _yt_opts()
    opts["format"] = "bestaudio/best"

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


async def get_video_stream(url: str) -> str:
    opts = _yt_opts()
    opts["format"] = "bestvideo[height<=360]+bestaudio/best"

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


# ======================================================
# VOICE CHAT HELPERS
# ======================================================

async def play_audio(call: PyTgCalls, chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        MediaStream(
            stream_url,
            audio_quality=AudioQuality.HIGH
        )
    )


async def play_video(call: PyTgCalls, chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        MediaStream(
            stream_url,
            audio_quality=AudioQuality.HIGH,
            video_quality=VideoQuality.MEDIUM
        )
    )


async def stop_stream(call: PyTgCalls, chat_id: int):
    try:
        await call.leave_group_call(chat_id)
    except Exception:
        pass


# ======================================================
# PLAYER UI
# ======================================================

def player_buttons():
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
                InlineKeyboardButton("❌ Close", callback_data="close")
            ]
        ]
    )


def now_playing_text(title: str, user):
    return (
        f"🎵 **Now Playing**\n\n"
        f"**Title:** {title}\n"
        f"**Requested by:** {user.mention}"
    )


# ======================================================
# INIT
# ======================================================

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils ready")
