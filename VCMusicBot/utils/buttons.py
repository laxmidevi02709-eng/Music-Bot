"""Inline-keyboard helpers."""
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from VCMusicBot import SUPPORT_URL


def player_markup(video_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏪ -10s",  callback_data="seekback"),
            InlineKeyboardButton("⏸ Pause",  callback_data="pause"),
            InlineKeyboardButton("▶️ Resume", callback_data="resume"),
            InlineKeyboardButton("⏩ +10s",  callback_data="seekfwd"),
        ],
        [
            InlineKeyboardButton("⏭ Skip",   callback_data="skip"),
            InlineKeyboardButton("⏹ Stop",   callback_data="stop"),
        ],
        [
            InlineKeyboardButton("🔗 YouTube Link", url=video_link),
            InlineKeyboardButton("💬 Support",      url=SUPPORT_URL),
        ],
    ])


def start_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Add me to your Group",
                                 url="https://t.me/share/url?url=Add%20me%20to%20your%20group&text=I%27m%20a%20premium%20VC%20music%20bot"),
        ],
        [
            InlineKeyboardButton("📖 Help & Commands", callback_data="help"),
            InlineKeyboardButton("💬 Support",         url=SUPPORT_URL),
        ],
    ])


def help_back_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("« Back", callback_data="back_start")]])
