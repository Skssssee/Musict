
# ======================================================
# utils/utils_system.py
# FIXED & STABLE FOR py-tgcalls 2.x
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional, Dict

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioVideoPiped
from pytgcalls.types import HighQualityAudio, MediumQualityVideo

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
# SEND LOG TO LOGGER GC
# ======================================================

async def send_log(bot, text: str):
    if not LOGGER_ID:
        return
    try:
        await bot.send_message(LOGGER_ID, f"📜 **MusicBot Log**\n\n{text}")
    except Exception as e:
        LOGGER.error(f"Log send failed: {e}")


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
        LOGGER.error(f"Cookie error: {e}")


# ======================================================
# YT-DLP (NO DOWNLOAD, DIRECT STREAM)
# ======================================================

def yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }


async def get_audio_stream(query: str) -> str:
    with yt_dlp.YoutubeDL({**yt_opts(), "format": "bestaudio"}) as ydl:
        return ydl.extract_info(query, download=False)["url"]


async def get_video_stream(query: str) -> str:
    with yt_dlp.YoutubeDL({**yt_opts(), "format": "bestvideo[height<=360]+bestaudio"}) as ydl:
        return ydl.extract_info(query, download=False)["url"]


# ======================================================
# PYTGCALLS INIT (NO CIRCULAR IMPORT)
# ======================================================

call: Optional[PyTgCalls] = None

def init_pytgcalls(assistant_client):
    global call
    call = PyTgCalls(assistant_client)
    return call


# ======================================================
# VC CONTROLS
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
# INLINE UI
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
# INIT
# ======================================================

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils initialized")
