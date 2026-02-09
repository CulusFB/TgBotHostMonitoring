from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.keyboards.menu_kb import create_menu, host_menu_kb
from app.lexicon.lexicon import LEXICON_RU
from app.models.host import Host
from app.states.states import FSMHostForm, FSMHostEditForm
from app.config import logger, config

router = Router()


@router.message(StateFilter(FSMHostForm.name))
async def add_host_name(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU.get("host_address"))
    await state.set_state(FSMHostForm.address)
    await state.update_data(name=message.text)


@router.message(StateFilter(FSMHostForm.address))
async def add_host_address(message: Message, state: FSMContext):
    state_date = await state.get_data()
    config.HOSTS.add_host(Host(name=state_date.get('name'), address=message.text, status=False))
    logger.success(f"Добавлен новый хост имя: `{state_date.get('name')}`, адрес: `{message.text}`")
    await message.answer(text=LEXICON_RU.get("success_add_host"), reply_markup=create_menu())
    await state.clear()


@router.message(StateFilter(FSMHostEditForm.name))
async def edit_host_name(message: Message, state: FSMContext):
    state_date = await state.get_data()
    host = config.HOSTS.get_host(state_date.get('address'))
    old_name = host.name
    host.name = message.text
    config.HOSTS.edit_host(host)
    logger.info(f"Изменено имя хоста `{old_name}` -> `{host.name}`")
    await state.clear()
    await message.answer(text=LEXICON_RU.get("success_edit"), reply_markup=host_menu_kb(host))


@router.message(StateFilter(FSMHostEditForm.address))
async def edit_host_name(message: Message, state: FSMContext):
    state_date = await state.get_data()
    host = config.HOSTS.get_host(state_date.get('address'))
    old_address = host.address
    host.address = message.text
    config.HOSTS.edit_host(host)
    logger.info(f"Изменён адрес хоста `{old_address}` -> `{host.address}`")
    await state.clear()
    await message.answer(text=LEXICON_RU.get("success_edit"), reply_markup=host_menu_kb(host))
