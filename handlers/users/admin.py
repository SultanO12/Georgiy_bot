import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from keyboards.default.main_panel import main_admin_markup, cancellations
from keyboards.default.chapter import chap_markup, addcat_markup
from states.send_msg import *
from states.admin_state import *

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("База очищена!")

@dp.message_handler(text="🔻Меню", user_id=ADMINS, state=EditChap.chapter)
@dp.message_handler(text="/panel", user_id=ADMINS, state='*')
async def do_admin_panel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Добро пожаловать в панель администратора!", reply_markup=main_admin_markup)

@dp.message_handler(text="👥 Всего пользователей", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[-1])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)

@dp.message_handler(text="📋 Разделы", user_id=ADMINS)
async def do_cat(message: types.Message, state: FSMContext):
    await state.finish()
    chapters = await db.select_all_chapters()
    
    msg = '<b>Разделы:</b>\n\n'
    if chapters:
        for chapter in chapters:
            msg += f"{chapter['id']}. {chapter['chapter_name']}\n"
        markup = await chap_markup()
        await message.answer(msg, reply_markup=markup)

        await EditChap.chapter.set()

@dp.message_handler(text="🔙 Назад", user_id=ADMINS, state=EditChap.chapter)
async def back_1(message: types.Message, state: FSMContext):
    await state.finish()
    chapters = await db.select_all_chapters()
    
    msg = '<b>Разделы:</b>\n\n'
    if chapters:
        for chapter in chapters:
            msg += f"{chapter['id']}. {chapter['chapter_name']}\n"
        markup = await chap_markup()
        await message.answer(msg, reply_markup=markup)

        await EditChap.chapter.set()

@dp.message_handler(state=EditChap.chapter, user_id=ADMINS)
async def get_chap(message: types.Message, state: FSMContext):
    chapter = message.text

    chapters = await db.select_all_chapters()
    chapter_id = ''
    for chap in chapters:
        if chapter == str(chap['chapter_name']):
            await state.update_data({"chpter":chapter})
            await state.update_data({"chapter_id":chap['id']})
            chapter_id += str(chap['id'])
            break

    msg = "<b>Категории:</b>\n\n"

    catigories = await db.select_all_categories()
    if catigories:
        for cat in catigories:
            if chapter_id == str(cat['chapter_id']):
                msg += f"{cat['cat_name']}"

        if len(msg) <= 14: 
            await message.answer(msg)
        else:
            await message.answer(f"Не найдено ни одного катигори по разделу {chapter}", reply_markup=addcat_markup)
    else:
        await message.answer("Не найдено ни одного категори:", reply_markup=addcat_markup)


    

@dp.message_handler(text="🗣 Рассылка", user_id=ADMINS)
async def send_mg(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Отправьте фото с текстом или просто текст:", reply_markup=cancellations)
    await GetMessage.msg.set()
    
@dp.message_handler(text="❌ Отменить", state=GetMessage.msg, user_id=ADMINS)
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Рассылка отменена!", reply_markup=main_admin_markup)

@dp.message_handler(content_types=['photo', 'text'], state=GetMessage.msg)
async def get_msg(message: types.Message, state: FSMContext):
    admin = message.from_user.id
    users = await db.select_all_users()

    if message.photo:
        photo_id = message.photo[-1]['file_id']
        caption = message.caption

        for user in users:
            try:
                await bot.send_photo(user[-1], photo=photo_id, caption=caption)
                await asyncio.sleep(0.05)
            except:
                await message.answer(f"Рассылка не отправлено id - {user[-1]}")
    else:
        msg = message.text

        for user in users:
            try:
                await bot.send_message(user[-1], msg)
                await asyncio.sleep(0.05)
            except:
                await message.answer(f"Рассылка не отправлено id - {user[-1]}")

    await state.finish()
    await message.answer("Рассылка успешно отправлена! ✅", reply_markup=main_admin_markup)
