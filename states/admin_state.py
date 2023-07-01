from aiogram.dispatcher.filters.state import StatesGroup, State

class EditChap(StatesGroup):
    chapter = State()
    cat = State()