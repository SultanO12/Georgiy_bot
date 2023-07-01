from aiogram.dispatcher.filters.state import StatesGroup, State

class GetInfoHoms(StatesGroup):
    home_name = State()
    home_photos = State()

class GetComent(StatesGroup):
    coment = State()

class GetInfoBron(StatesGroup):
    full_name = State()
    phone_num = State()
    date = State()
    count_perosons = State()
    check = State()