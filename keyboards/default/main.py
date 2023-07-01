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

homs_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
homs_cat_markup.add(KeyboardButton("🛕А-фрейм с купелью"), KeyboardButton("🏠 Дом на дереве"), KeyboardButton("🛕Высокий A-фрейм"))
homs_cat_markup.add(menu, bron)

raz_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
raz_cat_markup.add(KeyboardButton("Байдарки"), KeyboardButton("Квадроциклы"))
raz_cat_markup.add(menu)

nav_markup = ReplyKeyboardMarkup(resize_keyboard=True)
nav_markup.add(back, menu)

food_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
food_cat_markup.add(menu)

coment_markup = ReplyKeyboardMarkup(resize_keyboard=True)
coment_markup.add(KeyboardButton("✍️ Написать отзыв"), menu)

check_date = ReplyKeyboardMarkup(resize_keyboard=True)
check_date.add(KeyboardButton("Узнать свободные даты"))