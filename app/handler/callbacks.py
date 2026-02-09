import asyncio

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from app.config import logger
from app.config.config import config
from app.keyboards.menu_kb import host_list_kb, create_menu, host_menu_kb, edit_host_kb
from app.lexicon.lexicon import LEXICON_RU
from app.services.log_format import host_name_address
from app.services.ping_service import ping_host
from app.states.states import FSMHostForm, FSMHostEditForm

router = Router()


@router.callback_query(F.data == "host_list", F.from_user.id.in_(config.USERS))
async def host_list(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU.get("host_list"), reply_markup=host_list_kb())


@router.callback_query(F.data == "main_menu", F.from_user.id.in_(config.USERS))
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU.get('main_menu'),
                                     reply_markup=create_menu())


@router.callback_query(F.data == "add_host", F.from_user.id.in_(config.USERS))
async def add_host(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text=LEXICON_RU.get('host_name'))
    await state.set_state(FSMHostForm.name)


@router.callback_query(F.data.startswith("host_"), F.from_user.id.in_(config.USERS))
async def host_(callback: CallbackQuery):
    host_address = callback.data.replace('host_', '')
    host = config.HOSTS.get_host(host_address)
    available = '🟢' if host.status else '🔴'
    await callback.message.edit_text(text=f"*Имя:* {host.name}\n*Адрес:* {host.address}\n*Доступность:* {available}",
                                     reply_markup=host_menu_kb(host))


@router.callback_query(F.data.startswith("delete_host_"), F.from_user.id.in_(config.USERS))
async def delete_host(callback: CallbackQuery):
    host_address = callback.data.replace('delete_host_', '')
    host = config.HOSTS.get_host(host_address)
    config.HOSTS.remove_host(host)
    logger.info(f"Хост удалён {host_name_address(host)}")
    await callback.message.edit_text(text=LEXICON_RU.get("deleted_host") + host.name, reply_markup=host_list_kb())


@router.callback_query(F.data.startswith("check_host_"), F.from_user.id.in_(config.USERS))
async def check_host(callback: CallbackQuery):
    host_address = callback.data.replace('check_host_', '')
    host = config.HOSTS.get_host(host_address)
    logger.info(f"Ручной запуск проверки хоста {host_name_address(host)}")
    await callback.message.edit_text(text="Подождите идёт проверка доступности")
    try:
        result = await ping_host(host.address)
        host.status = True
        logger.info(f"Хост доступен {host_name_address(host)}")
        await callback.message.edit_text(text=f"Хост *{host.name}* доступен 🟢", reply_markup=host_menu_kb(host))
        config.HOSTS.edit_host(host)
    except ValueError:
        host.status = False
        config.HOSTS.edit_host(host)
        logger.warning(f"Для хоста `{host.name}` имя узла или имя службы `{host.address}` не указано или неизвестно")
        await callback.message.edit_text(text=
                                         f"Для хоста *{host.name}* имя узла или имя службы *{host.address}* не указано или неизвестно 🔴",
                                         reply_markup=host_menu_kb(host))


    except TimeoutError:
        host.status = False
        config.HOSTS.edit_host(host)
        logger.warning(f"Хост недоступен {host_name_address(host)}")
        await callback.message.edit_text(text=f"Хост *{host.name}* недоступен 🔴", reply_markup=host_menu_kb(host))


@router.callback_query(F.data.startswith("edit_host_"), F.from_user.id.in_(config.USERS))
async def edit_host(callback: CallbackQuery):
    host_address = callback.data.replace('edit_host_', '')
    host = config.HOSTS.get_host(host_address)
    await callback.message.edit_text(text="Выберите изменяемый параметр", reply_markup=edit_host_kb(host))


@router.callback_query(F.data.startswith("edit_name_host_"), F.from_user.id.in_(config.USERS))
async def edit_host_name(callback: CallbackQuery, state: FSMContext):
    host_address = callback.data.replace('edit_name_host_', '')
    host = config.HOSTS.get_host(host_address)
    await callback.message.answer(text=LEXICON_RU.get("host_name"))
    await state.set_state(FSMHostEditForm.name)
    await state.update_data(address=host.address)


@router.callback_query(F.data.startswith("edit_address_host_"), F.from_user.id.in_(config.USERS))
async def edit_host_name(callback: CallbackQuery, state: FSMContext):
    host_address = callback.data.replace('edit_address_host_', '')
    host = config.HOSTS.get_host(host_address)
    await callback.message.answer(text=LEXICON_RU.get("host_address"))
    await state.set_state(FSMHostEditForm.address)
    await state.update_data(address=host.address)
