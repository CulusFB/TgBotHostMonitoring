from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message

from app.config.config import logger

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer('Привет! Это Telegram бот для мониторинга хостов.')
