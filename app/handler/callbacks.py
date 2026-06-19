import asyncio
from typing import Optional

from aiogram import Router, F, html
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from app.config import logger
from app.config.config import config
from app.keyboards.menu_kb import host_list_kb, create_menu, host_menu_kb, edit_host_kb
from app.lexicon.lexicon import LEXICON_RU
from app.models.host import Host
from app.services.log_format import host_name_address
from app.services.ping_service import ping_host
from app.states.states import FSMHostForm, FSMHostEditForm

router = Router()


async def resolve_host(callback: CallbackQuery, prefix: str) -> Optional[Host]:
    """Извлекает адрес из callback_data по префиксу и возвращает хост.

    Если хост не найден (например, удалён) — отвечает алертом и возвращает None.
    """
    host = config.HOSTS.get_host(callback.data.removeprefix(prefix))
    if host is None:
        await callback.answer(LEXICON_RU.get("host_not_found"), show_alert=True)
    return host


@router.callback_query(F.data == "host_list", F.from_user.id.in_(config.USERS))
async def host_list(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU.get("host_list"), reply_markup=host_list_kb())


@router.callback_query(F.data == "main_menu", F.from_user.id.in_(config.USERS))
async def main_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text=LEXICON_RU.get('main_menu'),
                                     reply_markup=create_menu())


@router.callback_query(F.data == "add_host", F.from_user.id.in_(config.USERS))
async def add_host(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text=LEXICON_RU.get('host_name'))
    await state.set_state(FSMHostForm.name)


@router.callback_query(F.data.startswith("host_"), F.from_user.id.in_(config.USERS))
async def host_(callback: CallbackQuery):
    host = await resolve_host(callback, "host_")
    if host is None:
        return
    await callback.answer()
    available = '🟢' if host.status else '🔴'
    await callback.message.edit_text(
        text=f"<b>Имя:</b> {html.quote(host.name)}\n"
             f"<b>Адрес:</b> {html.quote(host.address)}\n"
             f"<b>Доступность:</b> {available}",
        reply_markup=host_menu_kb(host))


@router.callback_query(F.data.startswith("delete_host_"), F.from_user.id.in_(config.USERS))
async def delete_host(callback: CallbackQuery):
    host = await resolve_host(callback, "delete_host_")
    if host is None:
        return
    await callback.answer()
    config.HOSTS.remove_host(host)
    logger.info(f"Хост удалён {host_name_address(host)}")
    await callback.message.edit_text(text=LEXICON_RU.get("deleted_host") + html.quote(host.name),
                                     reply_markup=host_list_kb())


@router.callback_query(F.data.startswith("check_host_"), F.from_user.id.in_(config.USERS))
async def check_host(callback: CallbackQuery):
    host = await resolve_host(callback, "check_host_")
    if host is None:
        return
    await callback.answer()
    logger.info(f"Ручной запуск проверки хоста {host_name_address(host)}")
    await callback.message.edit_text(text="Подождите идёт проверка доступности")
    try:
        result = await ping_host(host.address)
        host.status = True
        logger.info(f"Хост доступен {host_name_address(host)}")
        await callback.message.edit_text(text=f"Хост <b>{html.quote(host.name)}</b> доступен 🟢",
                                         reply_markup=host_menu_kb(host))
        config.HOSTS.edit_host(host)
    except ValueError:
        host.status = False
        config.HOSTS.edit_host(host)
        logger.warning(f"Для хоста `{host.name}` имя узла или имя службы `{host.address}` не указано или неизвестно")
        await callback.message.edit_text(
            text=f"Для хоста <b>{html.quote(host.name)}</b> имя узла или имя службы "
                 f"<b>{html.quote(host.address)}</b> не указано или неизвестно 🔴",
            reply_markup=host_menu_kb(host))


    except (TimeoutError, OSError):
        host.status = False
        config.HOSTS.edit_host(host)
        logger.warning(f"Хост недоступен {host_name_address(host)}")
        await callback.message.edit_text(text=f"Хост <b>{html.quote(host.name)}</b> недоступен 🔴",
                                         reply_markup=host_menu_kb(host))


@router.callback_query(F.data.startswith("edit_host_"), F.from_user.id.in_(config.USERS))
async def edit_host(callback: CallbackQuery):
    host = await resolve_host(callback, "edit_host_")
    if host is None:
        return
    await callback.answer()
    await callback.message.edit_text(text="Выберите изменяемый параметр", reply_markup=edit_host_kb(host))


@router.callback_query(F.data.startswith("edit_name_host_"), F.from_user.id.in_(config.USERS))
async def edit_host_name(callback: CallbackQuery, state: FSMContext):
    host = await resolve_host(callback, "edit_name_host_")
    if host is None:
        return
    await callback.answer()
    await callback.message.answer(text=LEXICON_RU.get("host_name"))
    await state.set_state(FSMHostEditForm.name)
    await state.update_data(address=host.address)


@router.callback_query(F.data.startswith("edit_address_host_"), F.from_user.id.in_(config.USERS))
async def edit_host_name(callback: CallbackQuery, state: FSMContext):
    host = await resolve_host(callback, "edit_address_host_")
    if host is None:
        return
    await callback.answer()
    await callback.message.answer(text=LEXICON_RU.get("host_address"))
    await state.set_state(FSMHostEditForm.address)
    await state.update_data(address=host.address)
