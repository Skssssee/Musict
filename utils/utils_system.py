# ======================================================
# utils/utils_system.py  (py-tgcalls 2.x FIXED)
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional, Dict

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from pytgcalls import PyTgCalls
from pytgcalls.types.stream import StreamAudio, StreamVideo
from pytgcalls.types.input_stream import AudioSource

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
        await bot.send_message(LOGGER_ID, f"📜 **MusicBot Log**\n\n{text}")
    except Exception as e:
        LOGGER.error(e)


# ======================================================
# COOKIES
# ======================================================

COOKIES_PATH = "cookies/cookies.txt"

async def load_cookies():
    if not COOKIE_URL:
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(COOKIE_URL) as resp:
            if resp.status == 200:
                os.makedirs("cookies", exist_ok=True)
                with open(COOKIES_PATH, "w", encoding="utf-8") as f:
                    f.write(await resp.text())
                LOGGER.info("Cookies loaded")


# ======================================================
# PYTGCALLS INIT (NO CIRCULAR IMPORT)
# ======================================================

call: Optional[PyTgCalls] = None

def init_pytgcalls(assistant):
    global call
    call = PyTgCalls(assistant)
    return call


# ======================================================
# YOUTUBE STREAM (NO DOWNLOAD)
# ======================================================

def yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "cookiefile": COOKIES_PATH if os.path.exists(COOKIES_PATH) else None,
    }


async def get_audio_stream(query: str) -> str:
    with yt_dlp.YoutubeDL({**yt_opts(), "format": "bestaudio"}) as ydl:
        info = ydl.extract_info(query, download=False)
        return info["url"]


async def get_video_stream(query: str) -> str:
    with yt_dlp.YoutubeDL(
        {**yt_opts(), "format": "bestvideo[height<=360]+bestaudio"}
    ) as ydl:
        info = ydl.extract_info(query, download=False)
        return info["url"]


# ======================================================
# STREAM CACHE
# ======================================================

STREAM_CACHE: Dict[str, str] = {}

def get_cached(q): return STREAM_CACHE.get(q)
def set_cache(q, u): STREAM_CACHE[q] = u


# ======================================================
# VOICE CHAT CONTROLS (FIXED)
# ======================================================

async def play_audio(chat_id: int, url: str):
    await call.join_group_call(
        chat_id,
        StreamAudio(AudioSource(url))
    )


async def play_video(chat_id: int, url: str):
    await call.join_group_call(
        chat_id,
        StreamVideo(AudioSource(url))
    )


async def stop_stream(chat_id: int):
    try:
        await call.leave_group_call(chat_id)
    except:
        pass


# ======================================================
# PLAYER UI
# ======================================================

def player_buttons():
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton("⏭ Skip", callback_data="skip"),
            InlineKeyboardButton("⏹ Stop", callback_data="stop"),
        ]]
    )


def now_playing_text(title, user):
    return f"🎶 **Now Playing**\n{title}\nRequested by {user.mention}"


# ======================================================
# INIT
# ======================================================

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils ready")
