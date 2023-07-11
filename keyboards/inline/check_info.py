from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_markup = InlineKeyboardMarkup()
check_markup.add(InlineKeyboardButton("Правильно ✅", callback_data="yes"), InlineKeyboardButton("Неправильно ❌", callback_data="no"))

check_info_markup = InlineKeyboardMarkup()
check_info_markup.add(InlineKeyboardButton("Да, всё верно! ✅", callback_data="yes"), InlineKeyboardButton("Нет, исправить ❌", callback_data="no"))