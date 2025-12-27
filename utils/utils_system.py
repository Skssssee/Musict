# ======================================================
# utils/utils_system.py  (PY-TGCALLS 2.x FIXED)
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional

from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
            async with session.get(COOKIE_URL) as r:
                if r.status == 200:
                    os.makedirs("cookies", exist_ok=True)
                    with open(COOKIES_PATH, "w") as f:
                        f.write(await r.text())
                    LOGGER.info("Cookies loaded")
    except Exception as e:
        LOGGER.error(e)


# ======================================================
# PYTGCALLS FACTORY (NO CIRCULAR IMPORT)
# ======================================================

_call: PyTgCalls | None = None

def get_call(assistant):
    global _call
    if _call is None:
        _call = PyTgCalls(assistant)
    return _call


# ======================================================
# YOUTUBE STREAM (NO DOWNLOAD)
# ======================================================

def _yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }


async def get_audio_stream(url: str) -> str:
    with yt_dlp.YoutubeDL(_yt_opts()) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


async def get_video_stream(url: str) -> str:
    opts = _yt_opts()
    opts["format"] = "bestvideo[height<=360]+bestaudio/best"
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]


# ======================================================
# VC HELPERS
# ======================================================

async def play_audio(call: PyTgCalls, chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        MediaStream(
            stream_url,
            audio_quality=AudioQuality.HIGH,
        )
    )


async def play_video(call: PyTgCalls, chat_id: int, stream_url: str):
    await call.join_group_call(
        chat_id,
        MediaStream(
            stream_url,
            audio_quality=AudioQuality.HIGH,
            video_quality=VideoQuality.MEDIUM,
        )
    )


async def stop_stream(call: PyTgCalls, chat_id: int):
    await call.leave_group_call(chat_id)


# ======================================================
# UI
# ======================================================

def player_buttons():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    )


def now_playing_text(title, user):
    return f"🎵 **Now Playing**\n{title}\nRequested by {user.mention}"


# ======================================================
# INIT
# ======================================================

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils ready")
