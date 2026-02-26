import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import config, logger
from app.handler import commands, callbacks, text
from app.services.ping_service import ping_host, ping_all_hosts


async def on_startup(bot: Bot):
    # Создаем задачу проверки хостов
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        ping_all_hosts,
        args=[config.HOSTS.names],
        trigger=IntervalTrigger(minutes=1),
        id='host_checker',
        replace_existing=True,
        next_run_time=datetime.now()
    )
    scheduler.start()
    # сохраняем ссылку
    bot.scheduler = scheduler
    logger.info("Scheduler started")


async def on_shutdown(bot: Bot):
    scheduler = getattr(bot, "scheduler", None)
    if scheduler:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler stopped")


async def main():
    bot = Bot(token=config.BOT.token, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.include_router(commands.router)
    dp.include_router(callbacks.router)
    dp.include_router(text.router)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    logger.info("Bot started")
    while True:
        try:
            await dp.start_polling(bot)
        except Exception:
            logger.exception("Polling crashed, restarting...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
