from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_admin_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_admin_markup.add(KeyboardButton("👥 Всего пользователей"))
main_admin_markup.row("📋 Разделы")
main_admin_markup.row("🗣 Рассылка")

cancellations = ReplyKeyboardMarkup(resize_keyboard=True)
cancellations.add("❌ Отменить")