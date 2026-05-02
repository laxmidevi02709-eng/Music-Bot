"""YouTube search + download helpers."""
import os
import asyncio
import yt_dlp
from youtubesearchpython2 import VideosSearch


from VCMusicBot import DOWNLOADS_DIR


async def yt_search(query: str):
    """Return first YouTube result dict for a query."""
    def _search():
        results = VideosSearch(query, limit=1).result().get("result", [])
        if not results:
            return None
        v = results[0]
        return {
            "id": v["id"],
            "title": v["title"],
            "duration": v.get("duration") or "Live",
            "link": v["link"],
            "channel": v["channel"]["name"],
            "thumbnail": v["thumbnails"][-1]["url"].split("?")[0],
            "views": v.get("viewCount", {}).get("text", "—"),
        }
    return await asyncio.to_thread(_search)


async def yt_download_audio(video_id: str) -> str:
    """Download best audio as m4a/webm and return the local file path."""
    out_tpl = os.path.join(DOWNLOADS_DIR, f"{video_id}.%(ext)s")

    def _dl():
        ydl_opts = {
            "format": "bestaudio[ext=m4a]/bestaudio/best",
            "outtmpl": out_tpl,
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "concurrent_fragment_downloads": 4,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=True
            )
            return ydl.prepare_filename(info)
    return await asyncio.to_thread(_dl)


async def yt_download_audio_mp3(video_id: str) -> str:
    """Download + convert to mp3 (used by /song command for sending file)."""
    out_tpl = os.path.join(DOWNLOADS_DIR, f"song_{video_id}.%(ext)s")

    def _dl():
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": out_tpl,
            "quiet": True,
            "no_warnings": True,
            "noplaylist": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}", download=True
            )
            base = ydl.prepare_filename(info)
            mp3 = os.path.splitext(base)[0] + ".mp3"
            return mp3
    return await asyncio.to_thread(_dl)
