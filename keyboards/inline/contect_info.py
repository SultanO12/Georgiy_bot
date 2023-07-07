from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_markup = InlineKeyboardMarkup()
admin_markup.add(InlineKeyboardButton(text="✍️ Написать администратору", url="https://t.me/tania_splav40"))

contact_markup = InlineKeyboardMarkup()
contact_markup.add(InlineKeyboardButton(text="📞 Связь с менеджером", url='https://t.me/tania_splav40'))