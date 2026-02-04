import asyncio
from app.config.config import config, logger
from app.handler import commands
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


async def main():
    # Создаем объекты бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    dp = Dispatcher()

    # Регистриуем роутеры в диспетчере
    dp.include_router(commands.router)

    # Запускаем полинг
    logger.info('Bot started')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
