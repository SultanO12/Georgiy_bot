from aiogram.dispatcher.filters.state import StatesGroup, State

class EditChap(StatesGroup):
    chapter = State()
    cat = State()
    check = State()

class CreatCatHome(StatesGroup):
    title = State()
    capton = State()
    photos = State()

class CreatCatRaz(StatesGroup):
    title = State()
    capton = State()
    photo = State()

class CreatCatAks(StatesGroup):
    title = State()
    capton = State()
