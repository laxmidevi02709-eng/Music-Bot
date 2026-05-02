"""
Run this ONCE locally to generate your Pyrogram v2 SESSION_STRING for the
assistant user account that will join voice chats.

    pip install pyrogram==2.0.106 tgcrypto==1.2.5
    python string_session.py
"""
from pyrogram import Client

print("\n✦ Pyrogram v2 String Session Generator ✦\n")
api_id = int(input("API_ID    : ").strip())
api_hash = input("API_HASH  : ").strip()

with Client("gen", api_id=api_id, api_hash=api_hash, in_memory=True) as app:
    s = app.export_session_string()
    print("\n✅ SESSION_STRING (copy this and put in .env):\n")
    print(s)
