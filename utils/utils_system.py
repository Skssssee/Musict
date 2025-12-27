# ======================================================
# utils/utils_system.py
# COMPLETE + FIXED (py-tgcalls 2.x)
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
import asyncio
from typing import Optional, Dict

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioVideoPiped
from pytgcalls.types import HighQualityAudio, MediumQualityVideo

from config import COOKIE_URL, LOGGER_ID


# ======================================================
# LOGGER SYSTEM
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
    Send logs to LOGGER_ID group/channel
    """
    if not LOGGER_ID:
        return
    try:
        await bot.send_message(LOGGER_ID, f"📜 **MusicBot Log**\n\n{text}")
    except Exception as e:
        LOGGER.error(f"Logger send failed: {e}")


# ======================================================
# SAFE REPLY (ANTI CRASH)
# ======================================================

async def safe_reply(message, text: str):
    try:
        await message.reply(text)
    except Exception:
        pass


# ======================================================
# COOKIE SYSTEM
# ======================================================

COOKIES_PATH = "cookies/cookies.txt"

async def load_cookies():
    """
    Download cookies from COOKIE_URL → cookies/cookies.txt
    """
    if not COOKIE_URL:
        LOGGER.warning("COOKIE_URL not set")
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COOKIE_URL) as resp:
                if resp.status == 200:
                    os.makedirs("cookies", exist_ok=True)
                    with open(COOKIES_PATH, "w", encoding="utf-8") as f:
                        f.write(await resp.text())
                    LOGGER.info("YouTube cookies loaded")
                else:
                    LOGGER.error("Cookie download failed")
    except Exception as e:
        LOGGER.error(f"Cookie error: {e}")


# ======================================================
# PYTGCALLS INIT (NO CIRCULAR IMPORT)
# ======================================================

call: Optional[PyTgCalls] = None

def init_pytgcalls(assistant_client):
    """
    Initialize PyTgCalls AFTER assistant starts
    """
    global call
    call = PyTgCalls(assistant_client)
    return call


# ======================================================
# YT-DLP (DIRECT STREAM – NO DOWNLOAD)
# ======================================================

def yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }


async def get_audio_stream(query: str) -> str:
    """
    Return direct audio stream URL
    """
    with yt_dlp.YoutubeDL({**yt_opts(), "format": "bestaudio"}) as ydl:
        info = ydl.extract_info(query, download=False)
        return info["url"]


async def get_video_stream(query: str) -> str:
    """
    Return direct video stream URL (<=360p)
    """
    with yt_dlp.YoutubeDL(
        {**yt_opts(), "format": "bestvideo[height<=360]+bestaudio"}
    ) as ydl:
        info = ydl.extract_info(query, download=False)
        return info["url"]


# ======================================================
# STREAM CACHE (IN-MEMORY)
# ======================================================
# Same song repeat → instant play

STREAM_CACHE: Dict[str, str] = {}

def get_cached(query: str) -> Optional[str]:
    return STREAM_CACHE.get(query)

def set_cache(query: str, stream_url: str):
    STREAM_CACHE[query] = stream_url


# ======================================================
# VOICE CHAT CONTROLS
# ======================================================

async def play_audio(chat_id: int, stream: str):
    await call.join_group_call(
        chat_id,
        AudioPiped(stream, HighQualityAudio())
    )


async def play_video(chat_id: int, stream: str):
    await call.join_group_call(
        chat_id,
        AudioVideoPiped(
            stream,
            HighQualityAudio(),
            MediumQualityVideo()
        )
    )


async def stop_stream(chat_id: int):
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


def now_playing_text(title: str, user):
    return (
        f"🎶 **Now Playing**\n\n"
        f"**Title:** {title}\n"
        f"**Requested by:** {user.mention}"
    )


# ======================================================
# INIT UTILS
# ======================================================

async def init_utils():
    """
    Called once at startup
    """
    await load_cookies()
    LOGGER.info("Utils system initialized")
