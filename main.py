"""Entry point for the Welcome24 Telegram bot."""

from __future__ import annotations

import asyncio
import logging
from urllib.parse import urlparse

from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import load_config

logger = logging.getLogger(__name__)


async def _start_polling(dp: Dispatcher, bot: Bot) -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Starting polling mode")
    await dp.start_polling(bot)


def _run_webhook(dp: Dispatcher, bot: Bot, webhook_url: str, host: str, port: int) -> None:
    parsed = urlparse(webhook_url)
    path = parsed.path or "/webhook"

    logger.info("Starting webhook mode on %s:%s (path: %s)", host, port, path)
    app = web.Application()
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=path)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=host, port=port)


def main() -> None:
    config = load_config()
    bot = Bot(token=config.telegram_token, parse_mode="HTML")
    dp = Dispatcher()

    from handlers import register_all_handlers

    register_all_handlers(dp)

    async def on_startup(bot_instance: Bot) -> None:
        me = await bot_instance.me()
        logger.info("Welcome24 bot ready as @%s", me.username)
        if config.webhook_url:
            await bot_instance.set_webhook(config.webhook_url, drop_pending_updates=True)

    dp.startup.register(on_startup)

    if config.webhook_url:
        _run_webhook(dp, bot, config.webhook_url, config.listen_host, config.listen_port)
    else:
        asyncio.run(_start_polling(dp, bot))


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot shut down")

