import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from keyboards.default.main_panel import *
from keyboards.default.chapter import *
from keyboards.inline.admin_inline import * 
from states.send_msg import *
from states.admin_state import *
import openpyxl

@dp.message_handler(text="ℹ️ Информация о пользователей", user_id=ADMINS, state='*')
@dp.message_handler(text="/exel", user_id=ADMINS, state='*')
async def do_admin_panel(message: types.Message, state: FSMContext):
    def createTable(data):
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet['A1'] = 'Telegram ID'
        sheet['B1'] = 'Имя'
        sheet['C1'] = 'Фамилия'
        sheet['D1'] = 'Дата рождение'
        sheet['E1'] = 'Телефон'
        for i, row in enumerate(data, start=2):
            if len(row) >= 5:
                sheet['A{}'.format(i)] = row[0]
                sheet['B{}'.format(i)] = row[1]
                sheet['C{}'.format(i)] = row[2]  
                sheet['D{}'.format(i)] = row[3]
                sheet['E{}'.format(i)] = row[4]

        wb.save('table.xlsx')


    users = await db.select_all_register_info()
    users_list = []

    for i in users:
        user_id = i['id']
        user = await db.select_user(id=int(user_id))
        telegram_id = user['telegram_id']
        users_list.append([str(telegram_id), str(i['name']), str(i['last_name']), str(i['date']), str(i['phone'])])
    createTable(users_list)

    with open('table.xlsx', 'rb') as file:
        await message.answer_document(file)

@dp.message_handler(text="/set_aks", user_id=ADMINS, state='*')
async def update_aks(message: types.Message, state: FSMContext):
    await message.answer("Text:")
    await CreatCatAks.capton.set()

@dp.message_handler(user_id=ADMINS, state=CreatCatAks.capton)
async def update_aks(message: types.Message, state: FSMContext):
    aks = await db.select_all_infomation3()
    if aks:
        await db.update_infomation3(id=aks['id'], caption=message.text)
        await message.answer("Акция обновлена")
    else:
        await db.add_infomation3(caption=message.text)
        await message.answer("Акция добавлен")
    await state.finish()

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await db.delete_users()
    await message.answer("База очищена!")

@dp.message_handler(text="/clean_exel", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await db.delete_reginfor()
    await message.answer("База очищена!")

@dp.message_handler(text="🔻Меню", user_id=ADMINS, state=EditChap.cat)
@dp.message_handler(text="🔻Меню", user_id=ADMINS, state=EditChap.chapter)
@dp.message_handler(text="/panel", user_id=ADMINS, state='*')
async def do_admin_panel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Добро пожаловать в панель администратора!", reply_markup=main_admin_markup)

@dp.message_handler(text="👥 Количество пользователей", user_id=ADMINS)
async def get_count_users(message: types.Message):
    users = await db.count_users()
    await message.answer(users)

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
    
    msg = f"<b>Разделы:</b>\n\n1. 🏡 Домики\n2. 🥳 Развлечение\n3. 🎉 Акции"
    await message.answer(msg, reply_markup=chapters_markup)
    await EditChap.chapter.set()


@dp.message_handler(text=["1", "2", "3"], state=EditChap.chapter, user_id=ADMINS)
async def get_cat(message: types.Message, state: FSMContext):
    cat = message.text
    if cat == "1":
        markup = await creat_homs_markup()
        await message.answer("Раздел 🏡 Домики:", reply_markup=markup)
        await state.update_data({"capter_name":"🏡 Домики"})
        await EditChap.cat.set()
    elif cat == "2":
        markup = await creat_markup_raz()
        await message.answer("Раздел 🥳 Развлечение:", reply_markup=markup)
        await state.update_data({"capter_name":"🥳 Развлечение"})
        await EditChap.cat.set()
    else:
        markup = await creat_markup_aks()
        await message.answer("Раздел 🎉 Акции:", reply_markup=markup)
        await state.update_data({"capter_name":"🎉 Акции"})
        await EditChap.cat.set()

@dp.message_handler(text="🔙 Назад", user_id=ADMINS, state=EditChap.cat)
async def back_1(message: types.Message, state: FSMContext):
    await state.finish()
    
    msg = f"<b>Разделы:</b>\n\n1. 🏡 Домики\n2. 🥳 Развлечение\n3. 🎉 Акции"
    await message.answer(msg, reply_markup=chapters_markup)
    await EditChap.chapter.set()

@dp.message_handler(text=['➕ Добавить категорию', '➕ Добавить aкцию'], state=EditChap.cat, user_id=ADMINS)
async def creat_cat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chapter_name = data['capter_name']

    if chapter_name == "🏡 Домики":
        await message.answer("Введите название домика:", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await CreatCatHome.title.set()

    elif chapter_name == "🥳 Развлечение":
        await message.answer("Введите название развлечения:", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await CreatCatRaz.title.set()

    elif chapter_name == "🎉 Акции":
        await message.answer("Введите название акции:", reply_markup=ReplyKeyboardRemove())
        await state.finish()
        await CreatCatAks.title.set()

@dp.message_handler(state=CreatCatHome.title, user_id=ADMINS)
async def get_title(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data({"title":message.text})
        await message.answer("Введите описание домика:")
        await CreatCatHome.capton.set()

@dp.message_handler(state=CreatCatHome.capton, user_id=ADMINS)
async def get_caption(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data({"caption":message.text})
        await message.answer("Введите минимум <b>2</b> фото ID через пробел:")
        await CreatCatHome.photos.set()


@dp.message_handler(state=CreatCatHome.photos, user_id=ADMINS)
async def get_caption(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data({"photos":message.text})
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("Без видео"))
        await message.answer("Введите Видео ID через пробел:")
        await CreatCatHome.video.set()

    

@dp.message_handler(state=CreatCatHome.photos, user_id=ADMINS)
async def get_caption(message: types.Message, state: FSMContext):
    if message.text:
        photos = message.text
        data = await state.get_data()
        title = data['title']
        caption = data['caption']
        if message.text == "Без видео":
            video = None
        else:
            video = message.text

        # await db.add_infomation(title, caption, photos, video)
        await state.finish()
        await message.answer("Информация успешно записана", reply_markup=main_admin_markup)

@dp.message_handler(state=CreatCatRaz.title, user_id=ADMINS)
async def get_title(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data({"title":message.text})
        await message.answer("Введите описание:")
        await CreatCatRaz.capton.set()

@dp.message_handler(state=CreatCatRaz.capton, user_id=ADMINS)
async def get_caption(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data({"caption":message.text})
        await message.answer("<b>1</b> фото ID:")
        await CreatCatRaz.photo.set()

@dp.message_handler(state=CreatCatRaz.photo, user_id=ADMINS)
async def get_caption(message: types.Message, state: FSMContext):
    if message.text:
        photos = message.text
        data = await state.get_data()
        title = data['title']
        caption = data['caption']

        await db.add_infomation2(title, caption, photos)
        await state.finish()
        await message.answer("Информация успешно записана", reply_markup=main_admin_markup)

@dp.message_handler(state=CreatCatAks.title, user_id=ADMINS)
async def get_title(message: types.Message, state: FSMContext):
    if message.text:
        await state.update_data({"title":message.text})
        await message.answer("Введите описание акции:")
        await CreatCatAks.capton.set()

@dp.message_handler(state=CreatCatAks.capton, user_id=ADMINS)
async def get_caption(message: types.Message, state: FSMContext):
    if message.text:
        data = await state.get_data()
        title = data['title']
        capton = message.text
        await db.add_infomation3(title, capton)

        await state.finish()
        await message.answer("Информация успешно записана", reply_markup=main_admin_markup)


@dp.message_handler(state=EditChap.cat, user_id=ADMINS)
async def get_cat(message: types.Message, state: FSMContext):
    data = await state.get_data()
    chapter_name = data['capter_name']
    
    if chapter_name == "🏡 Домики":
        titles = await db.select_all_infomation()
        for title in titles:
            if message.text == title['title']:
                await message.answer(f"Вы точно хотите удалить {title['title']}?", reply_markup=check_markup)
                await state.update_data({"title":message.text})
                await EditChap.check.set()
                break
    elif chapter_name == "🥳 Развлечение":
        titles = await db.select_all_infomation2()
        for title in titles:
            if message.text == title['title']:
                await message.answer(f"Вы точно хотите удалить {title['title']}?", reply_markup=check_markup)
                await state.update_data({"title":message.text})
                await EditChap.check.set()
                break
    elif chapter_name == "🎉 Акции":
        titles = await db.select_all_infomation3()
        for title in titles:
            if message.text == title['title']:
                await message.answer(f"Вы точно хотите удалить {title['title']}?", reply_markup=check_markup)
                await state.update_data({"title":message.text})
                await EditChap.check.set()
                break

@dp.callback_query_handler(text=['yes', 'no'], state=EditChap.check, user_id=ADMINS)
async def check3(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()

    data = await state.get_data()
    chapter_name = data['capter_name']
    title = data['title']
    if call.data == 'yes':
        if chapter_name == "🏡 Домики":
            await db.delete_info(title)
            await state.finish()
            await call.message.answer("Успешно удалено!", reply_markup=main_admin_markup)
        elif chapter_name == "🥳 Развлечение":
            await db.delete_info2(title)
            await state.finish()
            await call.message.answer("Успешно удалено!", reply_markup=main_admin_markup)
        elif chapter_name == "🎉 Акции":
            await db.delete_info3(title)
            await state.finish()
            await call.message.answer("Успешно удалено!", reply_markup=main_admin_markup)
    else:
        await call.message.answer("Информация не удалено!")
        await state.finish()
    
        msg = f"<b>Разделы:</b>\n\n1. 🏡 Домики\n2. 🥳 Развлечение\n3. 🎉 Акции"
        await call.message.answer(msg, reply_markup=chapters_markup)
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

@dp.message_handler(text="🗣 Рассылка (фото)", user_id=ADMINS)
async def rass(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Отправьте фото ID <b>через пробел</b>:", reply_markup=cancellations)
    await GetMessage.msg2.set()

@dp.message_handler(content_types=['text'], state=GetMessage.msg2)
async def get_msg(message: types.Message, state: FSMContext):
    photo_ids = message.text.split()
    await state.update_data({"photo_ids":photo_ids})
    await message.answer("Отправтье описание:")
    await GetMessage.caption.set()

@dp.message_handler(content_types=['text'], state=GetMessage.caption)
async def get_msg(message: types.Message, state: FSMContext): 
    data = await state.get_data()
    photo_ids = data['photo_ids'][:-1]
    photo_id_caption = photo_ids[-1]
    caption = message.text

    sms = await message.answer("Рассылка начался...")
    users = await db.select_all_users()

    media = types.MediaGroup()
    for photo_id in photo_ids:
        media.attach_photo(photo=photo_id)
    media.attach_photo(photo=photo_id_caption, caption=caption)
    
    for user in users:
            try:
                await bot.send_media_group(user[-1], media=media)
                await asyncio.sleep(0.05)
            except:
                await message.answer(f"Рассылка не отправлено id - {user[-1]}")
    
    await bot.delete_message(chat_id=message.from_user.id, message_id=sms.message_id)
    await state.finish()
    await message.answer("Рассылка успешно отправлена! ✅", reply_markup=main_admin_markup)

@dp.message_handler(text="🗣 Рассылка", user_id=ADMINS)
async def send_mg(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Отправьте фото/видео с текстом или просто текст:", reply_markup=cancellations)
    await GetMessage.msg.set()
    
@dp.message_handler(text="❌ Отменить", state=[GetMessage.msg, GetMessage.msg2], user_id=ADMINS)
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Рассылка отменена!", reply_markup=main_admin_markup)

@dp.message_handler(content_types=['photo', 'video', 'text'], state=GetMessage.msg)
async def get_msg(message: types.Message, state: FSMContext):
    sms = await message.answer("Рассылка начался...")
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
    elif message.text:
        msg = message.text

        for user in users:
            try:
                await bot.send_message(user[-1], msg)
                await asyncio.sleep(0.05)
            except:
                await message.answer(f"Рассылка не отправлено id - {user[-1]}")
    else:
        video_id = message.video.file_id
        caption = message.caption

        for user in users:
            try:
                await bot.send_video(user[-1], video=video_id, caption=caption)
                await asyncio.sleep(0.05)
            except:
                await message.answer(f"Рассылка не отправлено id - {user[-1]}")

    await bot.delete_message(chat_id=message.from_user.id, message_id=sms.message_id)
    await state.finish()
    await message.answer("Рассылка успешно отправлена! ✅", reply_markup=main_admin_markup)

@dp.message_handler(text="🆔 Получить фото ID", user_id=ADMINS)
async def do_cat(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Отправьте фото:")

@dp.message_handler(content_types=['photo'], user_id=ADMINS)
async def get_file_id(message: types.Message):
    await message.answer(message.photo[-1]['file_id'])

# @dp.message_handler(content_types=['video'], user_id=ADMINS)
# async def process_video(message: types.Message):
#     video_file_id = message.video.file_id
#     await message.reply(video_file_id)
