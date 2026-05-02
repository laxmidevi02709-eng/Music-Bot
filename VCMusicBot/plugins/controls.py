"""Pause / resume / skip / stop / queue commands."""
import os
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream, AudioQuality

from VCMusicBot import bot, calls, LOGGER
from VCMusicBot.utils import queue as Q
from VCMusicBot.utils.fonts import premium, italic_premium


@bot.on_message(filters.command("pause") & filters.group)
async def pause_cmd(_, m: Message):
    try:
        await calls.pause_stream(m.chat.id)
        await m.reply_text(f"⏸ {premium('Paused')}")
    except Exception as e:
        await m.reply_text(f"❌ {e}")


@bot.on_message(filters.command("resume") & filters.group)
async def resume_cmd(_, m: Message):
    try:
        await calls.resume_stream(m.chat.id)
        await m.reply_text(f"▶️ {premium('Resumed')}")
    except Exception as e:
        await m.reply_text(f"❌ {e}")


@bot.on_message(filters.command("stop") & filters.group)
async def stop_cmd(_, m: Message):
    try:
        await calls.leave_call(m.chat.id)
    except Exception:
        pass
    Q.clear(m.chat.id)
    await m.reply_text(f"⏹ {premium('Stopped')} {italic_premium('and queue cleared.')}")


@bot.on_message(filters.command("skip") & filters.group)
async def skip_cmd(_, m: Message):
    chat_id = m.chat.id
    nxt = Q.pop_next(chat_id)
    if not nxt:
        try:
            await calls.leave_call(chat_id)
        except Exception:
            pass
        Q.clear(chat_id)
        return await m.reply_text(f"⏭ {italic_premium('Queue empty — left voice chat.')}")

    try:
        await calls.play(chat_id, MediaStream(nxt["file"], audio_parameters=AudioQuality.HIGH))
        Q.NOW_PLAYING[chat_id] = nxt
        Q.SEEK_OFFSET[chat_id] = 0
        await m.reply_text(
            f"⏭ {premium('Skipped')} → {italic_premium('Now playing')}: <b>{nxt['title']}</b>"
        )
    except Exception as e:
        LOGGER.exception("skip failed")
        await m.reply_text(f"❌ {e}")


@bot.on_message(filters.command("queue") & filters.group)
async def queue_cmd(_, m: Message):
    chat_id = m.chat.id
    np = Q.NOW_PLAYING.get(chat_id)
    if not np and not Q.length(chat_id):
        return await m.reply_text(italic_premium("Nothing playing."))
    txt = f"🎶 {premium('Queue')}\n\n"
    if np:
        txt += f"▶️ <b>Now</b>: {np['title']}\n\n"
    for i, t in enumerate(Q.QUEUES[chat_id], 1):
        txt += f"{i}. {t['title']}\n"
    await m.reply_text(txt)
