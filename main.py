import asyncio
from app.config.config import config, logger
from app.handler import commands
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


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
    await asyncio.sleep(10)


async def main():
    await asyncio.gather(
        tim(), bot_start())


if __name__ == '__main__':
    asyncio.run(main())
