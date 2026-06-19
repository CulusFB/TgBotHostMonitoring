from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.config.config import config, logger


async def send_all_users(msg: str, users: list[int] = config.USERS, bot: Bot = config.BOT):
    for user in users:
        try:
            await bot.send_message(user, msg)
        except TelegramAPIError as e:
            logger.error(f"Ошибка отправки пользователю {user}: {e}")
