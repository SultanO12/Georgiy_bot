from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS
from utils.extra_datas import make_title
from keyboards.default.main import main_markup


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()

    full_name = message.from_user.full_name
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=full_name,
            username=message.from_user.username,
        )
        # Сообщаем админу
        count = await db.count_users()
        msg = f"[{make_title(user['full_name'])}](tg://user?id={user['telegram_id']}) добавлен на базу\.\nНа базе {count} пользователей\."
        await bot.send_message(chat_id=ADMINS[0], text=msg, parse_mode=types.ParseMode.MARKDOWN_V2)
    else:
        await bot.send_message(chat_id=ADMINS[0], text=f"[{make_title(full_name)}](tg://user?id={message.from_user.id}) добавлен в базу ранее", disable_web_page_preview=True, parse_mode=types.ParseMode.MARKDOWN_V2)
    await message.answer(f"Добро пожаловать\! {make_title(full_name)}", parse_mode=types.ParseMode.MARKDOWN_V2, reply_markup=main_markup)
