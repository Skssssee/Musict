# utils/utils_system.py
# WORKING WITH py-tgcalls 2.2.0rc1

import os
import logging
import aiohttp
import yt_dlp

from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioStream, VideoStream

from assistants.assistant_system import assistant
from config import COOKIE_URL, LOGGER_ID

# ================= LOGGER =================

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
    if LOGGER_ID:
        try:
            await bot.send_message(LOGGER_ID, text)
        except:
            pass


# ================= COOKIES =================

COOKIES_PATH = "cookies/cookies.txt"

async def load_cookies():
    if not COOKIE_URL:
        return
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(COOKIE_URL) as r:
                if r.status == 200:
                    os.makedirs("cookies", exist_ok=True)
                    with open(COOKIES_PATH, "w") as f:
                        f.write(await r.text())
                    LOGGER.info("Cookies loaded")
    except Exception as e:
        LOGGER.error(e)


# ================= PYTGCALLS =================

call = PyTgCalls(assistant)


# ================= YOUTUBE =================

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


# ================= VOICE CHAT =================

async def play_audio(chat_id: int, url: str):
    await call.join_group_call(chat_id, AudioStream(url))

async def play_video(chat_id: int, url: str):
    await call.join_group_call(chat_id, VideoStream(url))

async def stop_stream(chat_id: int):
    try:
        await call.leave_group_call(chat_id)
    except:
        pass


# ================= UI =================

def player_buttons():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("❌ Close", callback_data="close")]]
    )

def now_playing_text(title, user):
    return f"🎶 **Now Playing**\n{title}\nRequested by {user.mention}"

async def init_utils():
    await load_cookies()
    LOGGER.info("Utils ready")
