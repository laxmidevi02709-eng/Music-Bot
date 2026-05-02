# 🎵 Premium VC Music Bot

A premium **Telegram Voice Chat music bot** built with **Pyrogram v2 + PyTgCalls + yt-dlp**.
Searches songs on YouTube, streams them in group voice chats, and offers full inline-button playback control.

![preview](VCMusicBot/assets/start.jpg)

---

## ✨ Features

- 🎶 `/play <song>` — searches YouTube → picks first result → streams in VC
- ⚠️ Auto-detects when no VC is active and tells the user to start one
- 🖼 Posts the **YouTube thumbnail** with description + inline buttons
- ⏪ -10s • ⏩ +10s • ⏸ Pause • ▶️ Resume • ⏭ Skip • ⏹ Stop
- 🔗 "Open on YouTube" + 💬 "Support" buttons
- 📥 `/song <name>` — downloads & sends the **MP3 file** (no VC needed)
- 📜 Help & Start messages styled in a **premium font** (Unicode bold)
- 🪪 Beautiful start image & inline keyboard menu
- 🔁 Auto-plays next track from queue when current ends

---

## 📋 Commands

| Command | Description |
|---|---|
| `/start` | Welcome card with image |
| `/help` | Full command list (premium font) |
| `/play <query>` | Search & stream a song in the group VC |
| `/song <query>` | Send the song as MP3 file |
| `/pause` `/resume` `/skip` `/stop` | Playback control |
| `/queue` | Show upcoming queue |

---

## 🛠 Setup

### 1. Get credentials
- **API_ID** & **API_HASH** → https://my.telegram.org → API development tools
- **BOT_TOKEN** → from [@BotFather](https://t.me/BotFather)
- **SESSION_STRING** → an **assistant user account** that will join voice chats.
  Generate it locally:
  ```bash
  pip install pyrogram==2.0.106 tgcrypto==1.2.5
  python string_session.py
  ```

### 2. Add the assistant to your group
- The user account whose `SESSION_STRING` you used **must be a member** of any group where you want to play music.
- Start a Voice Chat in the group **before** running `/play`.
- Make sure the bot is also added (admin recommended).

---

## 🚀 Deploy on Render

This repo includes a ready `render.yaml` and `Dockerfile`.

### Option A — Blueprint (recommended)
1. Push this repo to GitHub.
2. On https://render.com → **New** → **Blueprint** → connect the repo.
3. Render auto-detects `render.yaml` and asks for env vars:
   `API_ID`, `API_HASH`, `BOT_TOKEN`, `SESSION_STRING`, `OWNER_ID` *(optional)*, `SUPPORT_URL` *(optional)*.
4. Deploy. Done. ✅

### Option B — Manual Worker
1. **New** → **Background Worker** → connect repo.
2. Environment: **Python 3**.
3. Build command:
   ```
   apt-get update && apt-get install -y ffmpeg && pip install -r requirements.txt
   ```
   *(if apt isn't allowed on your plan, switch to the Docker tab — it uses the included `Dockerfile`.)*
4. Start command:
   ```
   python -m VCMusicBot
   ```
5. Add the env vars listed above and deploy.

> ⚠️ **Important**: Render's free **web service** sleeps after inactivity. Use a **Background Worker** (free tier) so the bot stays online. Free worker has 750 hrs/month — enough for a single always-on bot.

---

## 🐳 Run locally (Docker)

```bash
cp .env.example .env   # fill in values
docker build -t vcmusicbot .
docker run --env-file .env vcmusicbot
```

## 🐍 Run locally (no Docker)

```bash
# Linux / WSL — needs ffmpeg installed (`sudo apt install ffmpeg`)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in values
python -m VCMusicBot
```

---

## 📁 Project structure

```
.
├── VCMusicBot/
│   ├── __init__.py        # clients & config
│   ├── __main__.py        # entry point
│   ├── assets/start.jpg   # premium start image
│   ├── plugins/
│   │   ├── start.py       # /start, /help (premium font)
│   │   ├── play.py        # /play  (VC streaming)
│   │   ├── song.py        # /song  (mp3 download)
│   │   ├── controls.py    # /pause /resume /skip /stop /queue
│   │   └── callbacks.py   # inline-button handler + auto-next
│   └── utils/
│       ├── youtube.py     # YouTube search + yt-dlp download
│       ├── queue.py       # per-chat queue
│       ├── buttons.py     # inline keyboards
│       └── fonts.py       # premium Unicode font helpers
├── requirements.txt
├── render.yaml
├── Dockerfile
├── Procfile
├── runtime.txt
├── string_session.py
└── .env.example
```

---

## ❤️ Credits
Built with [Pyrogram](https://docs.pyrogram.org), [PyTgCalls](https://pytgcalls.github.io), [yt-dlp](https://github.com/yt-dlp/yt-dlp).
