import asyncio
from datetime import datetime

from aiogram import Bot, Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config.config import config
from app.config.config import logger
from app.handler import commands
from app.services.ping_service import ping_host, ping_all_hosts


async def bot_start(bot: Bot = config.BOT):
    # Создаем задачу проверки хостов
    scheduler = AsyncIOScheduler()
    scheduler.add_job(func=ping_all_hosts, args=[config.HOSTS.names], trigger=IntervalTrigger(minutes=1),
                      id='host_checker',
                      replace_existing=True, next_run_time=datetime.now())
    scheduler.start()
    # Создаем объект диспетчера
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands.router)

    # Запускаем полинг
    logger.info('Bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(bot_start())
