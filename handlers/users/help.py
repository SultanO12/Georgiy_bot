from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram.dispatcher import FSMContext
from loader import dp


@dp.message_handler(CommandHelp(), state='*')
async def bot_help(message: types.Message, state: FSMContext):
    await state.finish()
    text = ("Команды: ",
            "/start - Запуск бота",
            "/menu - Меню",
            "/help - Помощь")
    
    await message.answer("\n".join(text))
