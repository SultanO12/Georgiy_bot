from aiogram.dispatcher.filters.state import StatesGroup, State

class GetMessage(StatesGroup):
    msg = State()