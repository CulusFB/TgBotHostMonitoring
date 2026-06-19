from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from app.config.config import config, logger


async def send_all_users(msg: str, users: Optional[list[int]] = None, bot: Optional[Bot] = None):
    if users is None:
        users = config.USERS
    if bot is None:
        bot = config.BOT
    for user in users:
        try:
            await bot.send_message(user, msg)
        except TelegramAPIError as e:
            logger.error(f"Ошибка отправки пользователю {user}: {e}")
