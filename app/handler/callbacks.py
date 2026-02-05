from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.config.config import config
from app.keyboards.menu_kb import host_list_kb, create_menu, host_menu_kb
from app.lexicon.lexicon import LEXICON_RU
from app.models.host import Hosts

router = Router()


@router.callback_query(F.data == "host_list")
async def host_list(callback: CallbackQuery):
    await callback.message.edit_text(text="📋 Список всех хостов", reply_markup=host_list_kb())


@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON_RU.get('main_menu'),
                                     reply_markup=create_menu())


# @router.callback_query(F.data == "add_host")
# async def add_host(callback: CallbackQuery):


@router.callback_query(F.data.startswith("host_"))
async def host_(callback: CallbackQuery):
    host_address = callback.data.replace('host_', '')
    host = config.HOSTS.get_host(host_address)
    available = '🟢' if host.status else '🔴'
    await callback.message.edit_text(text=f"*Имя:* {host.name}\n*Адрес:* {host.address}\n*Доступность:* {available}",
                                     reply_markup=host_menu_kb(host))


@router.callback_query(F.data.startswith("delete_host_"))
async def delete_host(callback: CallbackQuery):
    host_address = callback.data.replace('delete_host_', '')
    host = config.HOSTS.get_host(host_address)
    config.HOSTS.remove_host(host)
    print(config.HOSTS.names)
