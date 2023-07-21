from aiogram.dispatcher.filters.state import StatesGroup, State

class GetMessage(StatesGroup):
    msg = State()
    msg2 = State()
    caption = State()