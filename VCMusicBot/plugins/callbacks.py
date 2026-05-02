"""Inline-button callback handler — pause/resume/skip/stop/seek/help."""
from pyrogram import filters
from pyrogram.types import CallbackQuery
from pytgcalls.types import MediaStream, AudioQuality

from VCMusicBot import bot, calls, START_IMAGE, LOGGER
from VCMusicBot.utils import queue as Q
from VCMusicBot.utils.buttons import start_markup, help_back_markup
from VCMusicBot.utils.fonts import premium, italic_premium
from VCMusicBot.plugins.start import HELP_TEXT, START_TEXT


async def _seek(chat_id: int, delta: int, cq: CallbackQuery):
    track = Q.NOW_PLAYING.get(chat_id)
    if not track:
        return await cq.answer("Nothing playing.", show_alert=True)
    new_off = max(0, Q.SEEK_OFFSET.get(chat_id, 0) + delta)
    Q.SEEK_OFFSET[chat_id] = new_off
    try:
        await calls.play(
            chat_id,
            MediaStream(
                track["file"],
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=f"-ss {new_off}",
            ),
        )
        await cq.answer(f"{'⏪' if delta < 0 else '⏩'} {abs(delta)}s — now at {new_off}s")
    except Exception as e:
        LOGGER.exception("seek failed")
        await cq.answer(f"Seek failed: {e}", show_alert=True)


@bot.on_callback_query()
async def cb_router(_, cq: CallbackQuery):
    data = cq.data
    chat_id = cq.message.chat.id if cq.message else 0

    try:
        if data == "help":
            await cq.message.edit_caption(HELP_TEXT, reply_markup=help_back_markup())
            return await cq.answer()

        if data == "back_start":
            name = cq.from_user.mention
            try:
                await cq.message.edit_caption(
                    START_TEXT.format(name=name), reply_markup=start_markup()
                )
            except Exception:
                await cq.message.edit_text(
                    START_TEXT.format(name=name), reply_markup=start_markup()
                )
            return await cq.answer()

        if data == "pause":
            await calls.pause_stream(chat_id)
            return await cq.answer("⏸ Paused")

        if data == "resume":
            await calls.resume_stream(chat_id)
            return await cq.answer("▶️ Resumed")

        if data == "stop":
            try:
                await calls.leave_call(chat_id)
            except Exception:
                pass
            Q.clear(chat_id)
            return await cq.answer("⏹ Stopped", show_alert=False)

        if data == "skip":
            nxt = Q.pop_next(chat_id)
            if not nxt:
                try:
                    await calls.leave_call(chat_id)
                except Exception:
                    pass
                Q.clear(chat_id)
                return await cq.answer("Queue empty — left VC.", show_alert=True)
            await calls.play(chat_id, MediaStream(nxt["file"], audio_parameters=AudioQuality.HIGH))
            Q.NOW_PLAYING[chat_id] = nxt
            Q.SEEK_OFFSET[chat_id] = 0
            return await cq.answer(f"⏭ {nxt['title'][:40]}")

        if data == "seekback":
            return await _seek(chat_id, -10, cq)
        if data == "seekfwd":
            return await _seek(chat_id, +10, cq)

        await cq.answer()
    except Exception as e:
        LOGGER.exception("callback failed")
        await cq.answer(f"⚠️ {e}", show_alert=True)


# Auto-play next track when current ends
from pytgcalls import filters as pf
from pytgcalls.types import Update
try:
    from pytgcalls.types.stream import StreamAudioEnded
except Exception:
    StreamAudioEnded = None


@calls.on_update(pf.stream_end())
async def on_end(_, update: Update):
    chat_id = update.chat_id
    nxt = Q.pop_next(chat_id)
    if not nxt:
        try:
            await calls.leave_call(chat_id)
        except Exception:
            pass
        Q.clear(chat_id)
        return
    try:
        await calls.play(chat_id, MediaStream(nxt["file"], audio_parameters=AudioQuality.HIGH))
        Q.NOW_PLAYING[chat_id] = nxt
        Q.SEEK_OFFSET[chat_id] = 0
    except Exception:
        LOGGER.exception("auto-next failed")
