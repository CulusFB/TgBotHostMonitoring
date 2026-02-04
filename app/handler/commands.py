from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message

from app.config.config import logger, config

router = Router()


@router.message(CommandStart(), F.from_user.id.in_(config.USERS))
async def process_start_command(message: Message):
    logger.info(message.from_user.id)
    await message.answer('Привет! Это Telegram бот для мониторинга хостов.')
