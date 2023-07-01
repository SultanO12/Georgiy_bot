from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import dp, db

menu = KeyboardButton('🔻Меню')
back = KeyboardButton("🔙 Назад")

async def chap_markup():
  markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

  chapters = await db.select_all_chapters()
  for chap in chapters:
    markup.insert(KeyboardButton(f"{chap['chapter_name']}"))
  markup.add(menu)
  
  return markup

addcat_markup = ReplyKeyboardMarkup(resize_keyboard=True)
addcat_markup.add(KeyboardButton("➕ Добавить категорию"))
addcat_markup.add(back, menu)