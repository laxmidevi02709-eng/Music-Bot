"""/song — download the song as mp3 and send to user (no VC needed)."""
import os
from pyrogram import filters
from pyrogram.types import Message

from VCMusicBot import bot, LOGGER
from VCMusicBot.utils.youtube import yt_search, yt_download_audio_mp3
from VCMusicBot.utils.fonts import premium, italic_premium


@bot.on_message(filters.command("song"))
async def song_cmd(_, m: Message):
    if len(m.command) < 2:
        return await m.reply_text(f"❗ {premium('Usage')}: /song <song name>")

    query = m.text.split(None, 1)[1]
    status = await m.reply_text(f"🔎 {italic_premium('Searching YouTube …')}")

    track = await yt_search(query)
    if not track:
        return await status.edit_text("❌ No results found.")

    await status.edit_text(f"⬇️ {italic_premium('Downloading & converting to mp3 …')}")
    try:
        mp3 = await yt_download_audio_mp3(track["id"])
    except Exception as e:
        LOGGER.exception("song download failed")
        return await status.edit_text(f"❌ Failed: <code>{e}</code>")

    await status.edit_text(f"📤 {italic_premium('Uploading …')}")
    try:
        await m.reply_audio(
            audio=mp3,
            title=track["title"],
            performer=track["channel"],
            thumb=None,
            caption=(
                f"🎵 <b>{track['title']}</b>\n"
                f"⏱ {track['duration']}  •  👤 {track['channel']}\n"
                f"🔗 <a href='{track['link']}'>YouTube</a>"
            ),
        )
        await status.delete()
    finally:
        try:
            os.remove(mp3)
        except OSError:
            pass
