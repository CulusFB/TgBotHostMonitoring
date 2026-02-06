from aiogram.fsm.state import default_state, State, StatesGroup


class FSMHostForm(StatesGroup):
    name = State()
    address = State()
