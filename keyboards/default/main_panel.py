from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp, db, bot

menu = KeyboardButton("🔻Меню")
back = KeyboardButton("🔙 Назад")

main_admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin_markup.add(KeyboardButton("👥 Всего пользователей"))
main_admin_markup.row("📋 Разделы")
main_admin_markup.row("🗣 Рассылка")
main_admin_markup.row("🆔 Получить Photo ID")

cancellations = ReplyKeyboardMarkup(resize_keyboard=True)
cancellations.add("❌ Отменить")

chapters_markup = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton("1")
    ],[
        KeyboardButton("2")
    ],[
        KeyboardButton("3")
    ],
], resize_keyboard=True)

chapters_markup.add(menu)

async def creat_homs_markup():
    homs_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = await db.select_all_infomation()
    for button in buttons:
        homs_cat_markup.insert(KeyboardButton(f"{button['title']}"))
    homs_cat_markup.row("➕ Добавить категорию")
    homs_cat_markup.add(back, menu)
    return homs_cat_markup

async def creat_markup_raz():
    raz_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = await db.select_all_infomation2()
    for button in buttons:
        raz_cat_markup.insert(KeyboardButton(f"{button['title']}"))
    raz_cat_markup.row("➕ Добавить категорию")
    raz_cat_markup.add(back, menu)
    return raz_cat_markup

async def creat_markup_aks():
    raz_cat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = await db.select_all_infomation3()
    for button in buttons:
        raz_cat_markup.insert(KeyboardButton(f"{button['title']}"))
    raz_cat_markup.row("➕ Добавить aкцию")
    raz_cat_markup.add(back, menu)
    return raz_cat_markup
