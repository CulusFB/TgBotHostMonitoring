from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.config import config
from app.lexicon.lexicon import LEXICON_RU
from app.models.host import Host


def create_menu() -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.get("host_list_b"),
            callback_data="host_list"
        ))
    kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON_RU.get('add_host_b'),
            callback_data="add_host"
        ))

    return kb_builder.as_markup()


def host_list_kb(hosts: list[Host] = config.HOSTS.names) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    buttons = []
    for host in hosts:
        available = '🟢' if host.status else '🔴'
        buttons.append(
            InlineKeyboardButton(text=f"{host.name} {available}", callback_data=f"host_{host.address}"))
    kb_builder.row(*buttons, width=3)
    kb_builder.row(InlineKeyboardButton(text=LEXICON_RU.get('back_b'), callback_data="main_menu"))
    return kb_builder.as_markup()


def host_menu_kb(host: Host) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text=LEXICON_RU.get('check_b'), callback_data=f"check_host_{host.address}"))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_RU.get('edit_host_b'), callback_data=f"edit_host_{host.address}"),
                   InlineKeyboardButton(text=LEXICON_RU.get('delete_host_b'),
                                        callback_data=f"delete_host_{host.address}"))
    kb_builder.row(InlineKeyboardButton(text=LEXICON_RU.get('back_b'), callback_data="host_list"))
    return kb_builder.as_markup()
