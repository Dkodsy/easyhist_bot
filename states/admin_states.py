from aiogram.dispatcher.filters.state import StatesGroup, State


class Admins(StatesGroup):
    enter_text = State()
    check_text = State()
