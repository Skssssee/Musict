
# ======================================================
# plugins/plugins_system.py
# ALL BOT COMMANDS COMBINED
# ======================================================

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from app import bot

# ---- CORE (permissions, sudo, logger, chats) ----
from core.core_system import (
    owner_only,
    sudo_or_owner,
    is_sudo,
    add_chat,
    get_all_chats,
    add_sudo,
    remove_sudo,
    enable_logger,
    disable_logger,
    get_logger_chat,
)

# ---- UTILS (stream, vc, ui, logs) ----
from utils.utils_system import (
    LOGGER,
    send_log,
    get_audio_stream,
    get_video_stream,
    play_audio,
    play_video,
    stop_stream,
    player_buttons,
    now_playing_text,
)

import asyncio


# ======================================================
# /start
# ======================================================
@bot.on_message(filters.command("start"))
async def start_cmd(_, m: Message):
    add_chat(m.chat.id)

    await m.reply(
        "🎵 **MusicBot is Alive!**\n\n"
        "Available Commands:\n"
        "/play <yt link>\n"
        "/vplay <yt link>\n"
        "/pause /resume /skip /stop\n"
        "/ping"
    )


# ======================================================
# /help
# ======================================================
@bot.on_message(filters.command("help"))
async def help_cmd(_, m: Message):
    await m.reply(
        "🎧 **MusicBot Help**\n\n"
        "/play – YouTube audio stream\n"
        "/vplay – YouTube video stream (360p)\n"
        "/pause – pause stream\n"
        "/resume – resume stream\n"
        "/skip – skip current\n"
        "/stop – stop VC\n"
        "/ping – bot health\n"
        "/broadcast – sudo/owner only"
    )


# ======================================================
# /play (AUDIO)
# ======================================================
@bot.on_message(filters.command("play") & filters.group)
async def play_cmd(_, m: Message):
    add_chat(m.chat.id)

    if len(m.command) < 2:
        return await m.reply("❌ Give a YouTube link")

    query = m.text.split(None, 1)[1]

    try:
        stream = await get_audio_stream(query)
        await play_audio(m.chat.id, stream)

        await m.reply(
            now_playing_text("YouTube Audio", "Live", m.from_user),
            reply_markup=player_buttons()
        )

        # logger GC
        await send_log(
            bot,
            f"▶️ PLAY\nChat: {m.chat.title}\nUser: {m.from_user.mention}\nQuery: {query}"
        )

    except Exception as e:
        LOGGER.error(f"/play error: {e}")
        await m.reply("❌ Failed to play audio")


# ======================================================
# /vplay (VIDEO 360p)
# ======================================================
@bot.on_message(filters.command("vplay") & filters.group)
async def vplay_cmd(_, m: Message):
    add_chat(m.chat.id)

    if len(m.command) < 2:
        return await m.reply("❌ Give a YouTube link")

    query = m.text.split(None, 1)[1]

    try:
        stream = await get_video_stream(query)
        await play_video(m.chat.id, stream)

        await m.reply(
            now_playing_text("YouTube Video", "Live (360p)", m.from_user),
            reply_markup=player_buttons()
        )

        await send_log(
            bot,
            f"🎥 VPLAY\nChat: {m.chat.title}\nUser: {m.from_user.mention}\nQuery: {query}"
        )

    except Exception as e:
        LOGGER.error(f"/vplay error: {e}")
        await m.reply("❌ Failed to play video")


# ======================================================
# PLAYER CONTROLS (BASIC)
# ======================================================
@bot.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, m: Message):
    if not sudo_or_owner(m.from_user.id):
        return await m.reply("❌ Admin / Sudo only")

    await stop_stream(m.chat.id)
    await m.reply("⏹ Stream stopped")


# ======================================================
# INLINE BUTTON HANDLER
# ======================================================
@bot.on_callback_query()
async def callbacks(_, q: CallbackQuery):
    data = q.data

    if data == "close":
        await q.message.delete()


# ======================================================
# /ping
# ======================================================
@bot.on_message(filters.command("ping"))
async def ping_cmd(_, m: Message):
    await m.reply("🏓 Pong! Bot is healthy")


# ======================================================
# /sudo (ADD / REMOVE)
# ======================================================
@bot.on_message(filters.command("sudo"))
async def sudo_cmd(_, m: Message):
    if not owner_only(m.from_user.id):
        return await m.reply("❌ Owner only")

    if len(m.command) < 3:
        return await m.reply("Usage: /sudo add|remove user_id")

    action = m.command[1]
    user_id = int(m.command[2])

    if action == "add":
        add_sudo(user_id)
        await m.reply("✅ Sudo added")
    elif action == "remove":
        remove_sudo(user_id)
        await m.reply("✅ Sudo removed")


# ======================================================
# /issudo
# ======================================================
@bot.on_message(filters.command("issudo"))
async def issudo_cmd(_, m: Message):
    if not owner_only(m.from_user.id):
        return await m.reply("❌ Owner only")

    if len(m.command) < 2:
        return await m.reply("Usage: /issudo user_id")

    user_id = int(m.command[1])
    await m.reply("✅ YES" if is_sudo(user_id) else "❌ NO")


# ======================================================
# /logger on|off
# ======================================================
@bot.on_message(filters.command("logger"))
async def logger_cmd(_, m: Message):
    if not owner_only(m.from_user.id):
        return await m.reply("❌ Owner only")

    if len(m.command) < 2:
        return await m.reply("/logger on | off")

    if m.command[1] == "on":
        enable_logger(m.chat.id)
        await m.reply("✅ Logger enabled here")

    elif m.command[1] == "off":
        disable_logger()
        await m.reply("❌ Logger disabled")


# ======================================================
# /broadcast (TEXT / MEDIA)
# ======================================================
@bot.on_message(filters.command("broadcast"))
async def broadcast_cmd(_, m: Message):
    if not sudo_or_owner(m.from_user.id):
        return await m.reply("❌ Not allowed")

    if not m.reply_to_message:
        return await m.reply("Reply to a message to broadcast")

    chats = get_all_chats()
    sent = 0

    await m.reply(f"📣 Broadcasting to {len(chats)} chats...")

    for cid in chats:
        try:
            await m.reply_to_message.copy(cid)
            sent += 1
            await asyncio.sleep(0.3)
        except Exception:
            continue

    await m.reply(f"✅ Broadcast done\nSent: {sent}")
