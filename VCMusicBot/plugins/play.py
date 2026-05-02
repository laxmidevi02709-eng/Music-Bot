"""/play command — search YouTube and stream in voice chat."""
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls.types import MediaStream, AudioQuality
from pytgcalls.exceptions import NoActiveGroupCall

from VCMusicBot import bot, calls, LOGGER
from VCMusicBot.utils.youtube import yt_search, yt_download_audio
from VCMusicBot.utils.buttons import player_markup
from VCMusicBot.utils.fonts import premium, italic_premium
from VCMusicBot.utils import queue as Q


@bot.on_message(filters.command(["play", "p"]) & filters.group)
async def play_cmd(_, m: Message):
    if len(m.command) < 2 and not m.reply_to_message:
        return await m.reply_text(
            f"❗ {premium('Usage')}: /play <song name or YouTube link>"
        )

    query = m.text.split(None, 1)[1] if len(m.command) >= 2 else m.reply_to_message.text
    status = await m.reply_text(f"🔎 {italic_premium('Searching YouTube …')}")

    track = await yt_search(query)
    if not track:
        return await status.edit_text("❌ No results found.")

    await status.edit_text(f"⬇️ {italic_premium('Downloading audio …')}")
    try:
        file_path = await yt_download_audio(track["id"])
    except Exception as e:
        LOGGER.exception("Download failed")
        return await status.edit_text(f"❌ Download failed: <code>{e}</code>")

    track["file"] = file_path
    track["requested_by"] = m.from_user.mention if m.from_user else "—"

    chat_id = m.chat.id

    # Already streaming → enqueue
    if chat_id in Q.NOW_PLAYING:
        Q.push(chat_id, track)
        pos = Q.length(chat_id)
        await status.delete()
        return await m.reply_photo(
            photo=track["thumbnail"],
            caption=(
                f"✚ {premium('Added to Queue')} (#{pos})\n\n"
                f"🎵 <b>{track['title']}</b>\n"
                f"⏱ {track['duration']}  •  👤 {track['channel']}\n"
                f"🙋 Requested by: {track['requested_by']}"
            ),
        )

    # Not streaming → start now
    try:
        await calls.play(
            chat_id,
            MediaStream(file_path, audio_parameters=AudioQuality.HIGH),
        )
    except NoActiveGroupCall:
        return await status.edit_text(
            f"⚠️ {premium('Voice Chat is not active')}\n\n"
            f"{italic_premium('Please start a voice chat in this group first, then run /play again.')}"
        )
    except Exception as e:
        LOGGER.exception("calls.play failed")
        return await status.edit_text(f"❌ Stream failed: <code>{e}</code>")

    Q.NOW_PLAYING[chat_id] = track
    Q.SEEK_OFFSET[chat_id] = 0

    await status.delete()
    await m.reply_photo(
        photo=track["thumbnail"],
        caption=(
            f"🎶 {premium('Now Streaming in VC')}\n\n"
            f"🎵 <b>{track['title']}</b>\n"
            f"⏱ Duration: {track['duration']}\n"
            f"👤 Channel: {track['channel']}\n"
            f"👁 Views: {track['views']}\n"
            f"🙋 Requested by: {track['requested_by']}"
        ),
        reply_markup=player_markup(track["link"]),
    )
