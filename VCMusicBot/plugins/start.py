from pyrogram import filters
from pyrogram.types import Message

from VCMusicBot import bot, START_IMAGE
from VCMusicBot.utils.buttons import start_markup, help_back_markup
from VCMusicBot.utils.fonts import premium, italic_premium


START_TEXT = (
    f"✦  {premium('Welcome')} {{name}}  ✦\n\n"
    f"{italic_premium('I am your premium voice-chat music companion.')}\n\n"
    f"🎧 {premium('Crystal-clear audio')} streaming in group VCs\n"
    f"🔎 {premium('Smart YouTube search')} — just type the song name\n"
    f"⏯ {premium('Full playback control')} — pause / resume / skip / seek\n"
    f"📥 {premium('Direct song download')} — get the mp3 anywhere\n\n"
    f"Tap {premium('Help')} below to see all commands."
)

HELP_TEXT = (
    f"📖  {premium('COMMAND LIST')}\n"
    f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
    f"⌬ /start — {italic_premium('show welcome card')}\n"
    f"⌬ /help  — {italic_premium('this menu')}\n\n"
    f"🎵  {premium('Music in Voice Chat')} (use in group)\n"
    f"⌬ /play <song name or url> — {italic_premium('search & stream in VC')}\n"
    f"⌬ /pause  — pause current track\n"
    f"⌬ /resume — resume playback\n"
    f"⌬ /skip   — skip to next in queue\n"
    f"⌬ /stop   — stop & clear queue\n"
    f"⌬ /queue  — view upcoming tracks\n\n"
    f"📥  {premium('Download (no VC needed)')}\n"
    f"⌬ /song <song name> — {italic_premium('get the mp3 file')}\n\n"
    f"━━━━━━━━━━━━━━━━━━━━━━\n"
    f"{italic_premium('Tip: Start a Voice Chat first, then use /play.')}"
)


@bot.on_message(filters.command("start") & filters.private)
async def start_private(_, m: Message):
    await m.reply_photo(
        photo=START_IMAGE,
        caption=START_TEXT.format(name=m.from_user.mention),
        reply_markup=start_markup(),
    )


@bot.on_message(filters.command("start") & filters.group)
async def start_group(_, m: Message):
    await m.reply_text(
        f"✦ {premium('Premium Music Bot is online')} ✦\n\n"
        f"{italic_premium('Use /play <song name> in this group to start streaming in VC.')}",
        reply_markup=start_markup(),
    )


@bot.on_message(filters.command("help"))
async def help_cmd(_, m: Message):
    await m.reply_text(HELP_TEXT, reply_markup=help_back_markup(), disable_web_page_preview=True)
