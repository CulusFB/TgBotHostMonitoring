import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config.config import config
from app.config.config import logger
from app.handler import commands
from app.services.ping_service import ping_host


async def bot_start():
    # Создаем объекты бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
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
        await ping_host("fbhost-vilage.keenetic.pro")
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(
        tim(), bot_start())


if __name__ == '__main__':
    asyncio.run(main())
