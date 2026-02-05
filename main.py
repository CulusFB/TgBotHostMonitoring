import asyncio

from aiogram import Bot, Dispatcher

from app.config.config import config
from app.config.config import logger
from app.handler import commands
from app.services.ping_service import ping_host, ping_all_hosts


async def bot_start(bot: Bot = config.BOT):
    # Создаем объект диспетчера
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands.router)

    # Запускаем полинг
    logger.info('Bot started')
    await dp.start_polling(bot)


async def tim():
    # TODO: Сделано для тестирования асинхронного запускать, убрать в будущем
    logger.info("Sleeping async")
    while True:
        await ping_all_hosts(config.HOSTS.names)
        await asyncio.sleep(30)


async def main():
    await asyncio.gather(
        tim(), bot_start())


if __name__ == '__main__':
    asyncio.run(main())
