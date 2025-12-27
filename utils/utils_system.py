# utils/utils_system.py
# ======================================================
# ALL SHARED UTILS (LOGGER + VC + YT)
# ======================================================

import os
import logging
import aiohttp
import yt_dlp
from typing import Optional, Dict

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls

from utils.logger import LOGGER
from config import COOKIE_URL, LOGGER_ID

# ======================================================
# PYTGCALLS (LAZY INIT – NO CIRCULAR IMPORT)
# ======================================================

_call: Optional[PyTgCalls] = None

def get_call() -> PyTgCalls:
    global _call
    if _call is None:
        from assistants.assistant_system import assistant
        _call = PyTgCalls(assistant)
    return _call


# ======================================================
# LOGGER HELPERS
# ======================================================

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
# YOUTUBE STREAM FETCH (NO DOWNLOAD)
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
# VOICE CHAT CONTROLS (py-tgcalls 2.x)
# ======================================================

async def play_audio(chat_id: int, stream_url: str):
    call = get_call()
    await call.join_group_call(chat_id, stream_url)

async def play_video(chat_id: int, stream_url: str):
    call = get_call()
    await call.join_group_call(chat_id, stream_url)

async def stop_stream(chat_id: int):
    call = get_call()
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
        ]
    )


# ======================================================
# INIT
# ======================================================

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils system initialized")
