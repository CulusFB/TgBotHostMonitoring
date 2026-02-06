from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.menu_kb import create_menu
from app.lexicon.lexicon import LEXICON_RU
from app.models.host import Host
from app.states.states import FSMHostForm
from app.config import logger, config

router = Router()

simple_host = {}


@router.message(StateFilter(FSMHostForm.name))
async def add_host_name(message: Message, state: FSMContext):
    simple_host["name"] = message.text
    await message.answer(text=LEXICON_RU.get("host_address"))
    await state.set_state(FSMHostForm.address)


@router.message(StateFilter(FSMHostForm.address))
async def add_host_address(message: Message, state: FSMContext):
    config.HOSTS.add_host(Host(name=simple_host.get("name"), address=message.text, status=False))
    simple_host.clear()
    await message.answer(text=LEXICON_RU.get("success_add_host"), reply_markup=create_menu())
    await state.clear()
