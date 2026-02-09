from aiogram import Router, F
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup

from app.config import logger, config
from app.keyboards.menu_kb import create_menu
from app.lexicon.lexicon import LEXICON_RU

router = Router()


@router.message(CommandStart(), F.from_user.id.in_(config.USERS))
async def process_start_command(message: Message, state: FSMContext):
    logger.info(
        f"Пользователь id: `{message.from_user.id}` username: `{message.from_user.username}` использовал `/start`")
    await message.reply(text=LEXICON_RU.get('main_menu'), reply_markup=create_menu())
    await state.clear()


@router.message(Command('version'), F.from_user.id.in_(config.USERS))
async def bot_version(message: Message):
    await message.answer(f"Версия бота `{config.VERSION}`")
