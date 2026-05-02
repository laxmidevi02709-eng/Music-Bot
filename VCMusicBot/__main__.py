"""Entry point — `python -m VCMusicBot`"""
import asyncio
import importlib
import pkgutil

from VCMusicBot import bot, assistant, calls, LOGGER
from VCMusicBot import plugins as plugins_pkg


async def main():
    LOGGER.info("Starting Bot client …")
    await bot.start()
    me = await bot.get_me()
    LOGGER.info(f"✓ Bot online as @{me.username}")

    LOGGER.info("Starting Assistant userbot …")
    await assistant.start()
    a_me = await assistant.get_me()
    LOGGER.info(f"✓ Assistant online as {a_me.first_name} ({a_me.id})")

    LOGGER.info("Starting PyTgCalls …")
    await calls.start()
    LOGGER.info("✓ PyTgCalls ready")

    # Auto-load all plugin modules
    for _, mod_name, _ in pkgutil.iter_modules(plugins_pkg.__path__):
        importlib.import_module(f"VCMusicBot.plugins.{mod_name}")
        LOGGER.info(f"  ↳ loaded plugin: {mod_name}")

    LOGGER.info("🎵 Premium VC Music Bot is fully operational.")
    # Idle forever
    from pyrogram import idle
    await idle()

    await bot.stop()
    await assistant.stop()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(main())
    except KeyboardInterrupt:
        LOGGER.info("Shutting down…")
