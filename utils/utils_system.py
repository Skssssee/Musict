import os, logging, aiohttp, yt_dlp
from typing import Optional
from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import COOKIE_URL, LOGGER_ID

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(message)s",
    handlers=[logging.FileHandler("logs/musicbot.log"), logging.StreamHandler()]
)
LOGGER = logging.getLogger("MusicBot")

async def send_log(bot, text: str):
    if LOGGER_ID:
        try:
            await bot.send_message(LOGGER_ID, text)
        except Exception:
            pass

_call: Optional[PyTgCalls] = None

def get_call(assistant):
    global _call
    if _call is None:
        _call = PyTgCalls(assistant)
    return _call

def _yt_opts():
    return {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "cookiefile": os.path.exists("cookies/cookies.txt") and "cookies/cookies.txt"
    }

async def get_audio_stream(url):
    with yt_dlp.YoutubeDL(_yt_opts()) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]

async def get_video_stream(url):
    with yt_dlp.YoutubeDL(_yt_opts()) as ydl:
        info = ydl.extract_info(url, download=False)
        return info["url"]

async def play_audio(chat_id, stream):
    call = _call
    await call.join_group_call(
        chat_id,
        MediaStream(stream, audio_quality=AudioQuality.HIGH)
    )

async def play_video(chat_id, stream):
    call = _call
    await call.join_group_call(
        chat_id,
        MediaStream(stream, audio_quality=AudioQuality.HIGH, video_quality=VideoQuality.MEDIUM)
    )

async def stop_stream(chat_id):
    call = _call
    await call.leave_group_call(chat_id)

def player_buttons():
    return InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close", callback_data="close")]])

def now_playing_text(title, user):
    return f"🎵 **Now Playing**\n{title}\nRequested by {user.mention}"

async def init_utils():
    LOGGER.info("Utils ready")
