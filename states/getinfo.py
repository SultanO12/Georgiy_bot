from aiogram.dispatcher.filters.state import StatesGroup, State

class GetInfoHoms(StatesGroup):
    home_name = State()
    home_photos = State()

class GetInfoRaz(StatesGroup):
    raz_name = State()
    raz_photo_cvad = State()
    raz_cat_splav = State()
    raz_photo_splav = State()

class GetInfoAks(StatesGroup):
    aks_name = State()
    aks_caption = State()

class GetComent(StatesGroup):
    coment = State()

class GetInfoBron(StatesGroup):
    full_name = State()
    phone_num = State()
    date = State()
    count_perosons = State()
    check = State()

class GetRegInfo(StatesGroup):
    first_name = State()
    last_name = State()
    phone = State()