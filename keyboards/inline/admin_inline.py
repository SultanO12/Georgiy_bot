from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

check_markup = InlineKeyboardMarkup()
check_markup.add(InlineKeyboardButton("Да ✅", callback_data="yes"), InlineKeyboardButton("Нет ❌", callback_data="no"))