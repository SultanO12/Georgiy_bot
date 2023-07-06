from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from loader import dp, db, bot

menu = KeyboardButton("🔻Меню")
back = KeyboardButton("🔙 Назад")
bron = KeyboardButton("🛎 Забронировать")

main_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_markup.add(KeyboardButton("🏡 Домики"), KeyboardButton("🥳 Развлечение"), KeyboardButton("🍽 Где поесть"))
main_markup.row("🎉 Акции", "🙏 Отзывы", "🚗 Как добраться")
main_markup.row("📲 Контакты", "🛎 Забронировать")

async def cat_markup(capter_id):
    cats = await db.select_all_categories()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    for cat in cats:
        if capter_id == cat['chapter_id']:
            markup.insert(KeyboardButton(f"{cat['cat_name']}"))
    markup.add(menu, bron)
    return markup

getinfo_markup = ReplyKeyboardMarkup(resize_keyboard=True)
getinfo_markup.add(KeyboardButton("Смотреть фотографии"), bron)
getinfo_markup.add(back, menu)

async def creat_homs_markup():
    homs_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = await db.select_all_infomation()
    for button in buttons:
        homs_cat_markup.insert(KeyboardButton(f"{button['title']}"))
    homs_cat_markup.add(menu, bron)
    return homs_cat_markup

async def creat_markup_raz():
    raz_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    # buttons = await db.select_all_infomation2()
    # for button in buttons:
    #     raz_cat_markup.insert(KeyboardButton(f"{button['title']}"))
    # raz_cat_markup.add(menu)

    raz_cat_markup.add(KeyboardButton("Сплавы на байдарках"), KeyboardButton("КВАДРОЦИКЛЫ"))
    raz_cat_markup.add(menu, bron)
    
    return raz_cat_markup
    

async def creat_markup_aks():
    raz_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = await db.select_all_infomation3()
    for button in buttons:
        raz_cat_markup.insert(KeyboardButton(f"{button['title']}"))
    raz_cat_markup.add(menu)
    return raz_cat_markup

nav_markup = ReplyKeyboardMarkup(resize_keyboard=True)
nav_markup.add(back, menu)

food_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
food_cat_markup.add(menu)

coment_markup = ReplyKeyboardMarkup(resize_keyboard=True)
coment_markup.add(KeyboardButton("✍️ Написать отзыв"), menu)

check_date = ReplyKeyboardMarkup(resize_keyboard=True)
check_date.add(KeyboardButton("Узнать свободные даты"))

photos_markup = ReplyKeyboardMarkup(resize_keyboard=True)
photos_markup.add(KeyboardButton("Смотреть фотографии"), bron)
photos_markup.add(back, menu)