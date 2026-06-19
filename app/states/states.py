from aiogram.fsm.state import State, StatesGroup


class FSMHostForm(StatesGroup):
    name = State()
    address = State()


class FSMHostEditForm(StatesGroup):
    name = State()
    address = State()
