from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_markup = InlineKeyboardMarkup()
check_markup.add(InlineKeyboardButton("Правильно ✅", callback_data="yes"), InlineKeyboardButton("Неправильно ❌", callback_data="no"))