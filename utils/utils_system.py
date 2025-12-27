# ======================================================
# utils/utils_system.py
# COMPATIBLE WITH py-tgcalls 2.1.0
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional, Dict

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls

from assistants.assistant_system import assistant
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
# PYTGCALLS INIT (IMPORTANT)
# ======================================================

call = PyTgCalls(assistant)


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
        LOGGER.error(f"Cookie load failed: {e}")


# ======================================================
# YOUTUBE STREAM (NO DOWNLOAD)
# ======================================================

def _yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }


async def get_audio_stream(query: str) -> Optional[str]:
    with yt_dlp.YoutubeDL({**_yt_opts(), "format": "bestaudio"}) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


async def get_video_stream(query: str) -> Optional[str]:
    with yt_dlp.YoutubeDL({**_yt_opts(), "format": "best[height<=360]"}) as ydl:
        info = ydl.extract_info(query, download=False)
        return info.get("url")


# ======================================================
# VOICE CHAT CONTROL (CORRECT WAY)
# ======================================================

async def play_audio(chat_id: int, url: str):
    await call.join_group_call(
        chat_id,
        url,
        stream_type="audio"
    )


async def play_video(chat_id: int, url: str):
    await call.join_group_call(
        chat_id,
        url,
        stream_type="video"
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
                InlineKeyboardButton("⏭ Skip", callback_data="skip"),
                InlineKeyboardButton("⏹ Stop", callback_data="stop"),
            ],
            [InlineKeyboardButton("❌ Close", callback_data="close")]
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
    LOGGER.info("Utils initialized (py-tgcalls 2.1.0)")
