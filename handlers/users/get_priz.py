from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.getinfo import GetRegInfo
from keyboards.default.main import *
from keyboards.inline.check_info import *

@dp.message_handler(text="🎁 Получить подарок", state='*')
async def get_reg_info(message: types.Message, state: FSMContext):
    await state.finish()

    user = await db.select_user(telegram_id=message.from_user.id)
    reg_user = await db.select_register_info(user_id=int(user['id']))

    if reg_user is None:
      await message.answer("🖐 Как тебя зовут?", reply_markup=ReplyKeyboardRemove())
      await message.answer("⬇️")

      await GetRegInfo.check_first_name.set()

@dp.message_handler(state=GetRegInfo.check_first_name)
async def check_1(message: types.Message, state: FSMContext):
    if message.text:
      name = message.text
      await message.answer(f"Ваше имя \"{name}\", верно?", reply_markup=check_info_markup)
      await state.update_data({"name":name})
      await GetRegInfo.first_name.set()

@dp.callback_query_handler(text=['yes', 'no'], state=GetRegInfo.first_name)
async def get_name(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    name = data['name']
    if call.data == 'yes':
      
      await call.message.answer(f"🙌 {name}, очень приятно познакомиться с тобой!")
      await call.message.answer(f"У меня уже есть друг {name}, чтобы мне вас не перепутать, напиши свою фамилию")
      await call.message.answer("⬇️")

      await GetRegInfo.check_last_name.set()
    else:
        await call.message.answer("🖐 Как тебя зовут?", reply_markup=ReplyKeyboardRemove())
        await call.message.answer("⬇️")

        await GetRegInfo.check_first_name.set()

@dp.message_handler(state=GetRegInfo.check_last_name)
async def check_1(message: types.Message, state: FSMContext):
    if message.text:
      last_name = message.text
      await message.answer(f"Ваше фамилия \"{last_name}\", верно?", reply_markup=check_info_markup)
      await state.update_data({"last_name":last_name})
      await GetRegInfo.last_name.set()

@dp.callback_query_handler(text=['yes', "no"], state=GetRegInfo.last_name)
async def get_last_name(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        data = await state.get_data()
        name = data['name']

        await call.message.answer(f"{name}, у меня последний вопрос!\n\nНапиши свой телефон, что бы наш администратор ничего не перепутала, а то она может )", reply_markup=send_number_markup)
        await call.message.answer("⬇️")

        await GetRegInfo.phone.set()
    else:
        await call.message.answer(f"Напишите свою фамилию")
        await call.message.answer("⬇️")
        await GetRegInfo.check_last_name.set()

@dp.message_handler(content_types=['contact'], state=GetRegInfo.phone)
@dp.message_handler(state=GetRegInfo.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if message.text:
        phone = message.text
        data = await state.get_data()
        name = data['name']
        await state.update_data({"phone":phone})

        await message.answer("😍 Отлично!\n\n💖 Теперь мы стали ближе", reply_markup=get_date_markup)
        await message.answer(f"{name}, на ваш бонусный счет зачислено 1000 ₽. \n\nТы можешь ими воспользоваться у нас глэмпинге, при бронировании домиков и дополнительных услуг\n\n*см. условия применения в разделе \"Акции\"")
        await message.answer(f"{name}, ты можешь сказать мне по секрету, когда у тебя День рождения.  А когда ты решишь отметить его у нас, я 💫подарю тебе скидкуеще на 500 Рублей")

        await GetRegInfo.date.set()
    elif message.contact:
        phone = message.contact.phone_number
        data = await state.get_data()
        name = data['name']
        await state.update_data({"phone":phone})

        

        await message.answer("😍 Отлично!\n\n💖 Теперь мы стали ближе", reply_markup=get_date_markup)
        await message.answer(f"{name}, на ваш бонусный счет зачислено 1000 ₽. \n\nТы можешь ими воспользоваться у нас в глэмпинге, при бронировании домиков или дополнительных услуг\n\n*см. условия применения в разделе \"Акции\"")
        await message.answer(f"{name}, ты можешь сказать мне по секрету, когда у тебя День рождения.  А когда ты решишь отметить его у нас, я 💫подарю тебе скидку еще на 500 Рублей")

        await GetRegInfo.date.set()

@dp.message_handler(commands=['menu'], state=GetRegInfo.date)
@dp.message_handler(text="🔻Меню", state=GetRegInfo.date)
async def save_info(message: types.Message, state: FSMContext):
    data = await state.get_data()
    name = data['name']
    last_name = data['last_name']
    phone = data['phone']

    user_id = await db.select_user(telegram_id=int(message.from_user.id))
    await db.add_register_info(user_id['id'], name, last_name, phone)
    await state.finish()
    await message.answer_photo("AgACAgIAAxkBAAIgUGSsMdIyvjkOU5eZl59jfXa_-Gr5AAIKyzEbrclgSWjEkpUIb5i1AQADAgADeQADLwQ", caption="Переходи в меню и знакомься с нашей базой!\n\nОчень рекомендую зайти в \"<b>Домики</b>\" - \"<b>Домик на дереве</b>\" и в \"<b>Развлечения</b>\" - \"<b>Квадроциклы</b>\". Там тебя ждут 🔥 зажигательные 🔥 видеоролики\n\nА так же подпишись на наш основной ТГ канал: @splav40 - там самые актуальные новости и фото.", reply_markup=main_markup)

@dp.message_handler(text="🎁 Написать когда ДР", state=GetRegInfo.date)
async def get_date(message: types.Message, state: FSMContext):
    await message.answer("Напиши свой день рождения\nв формате\n22.07.1999", reply_markup=ReplyKeyboardRemove())
    await message.answer("⬇️")
    await GetRegInfo.get.set()
    

@dp.message_handler(state=GetRegInfo.get)
async def get(message: types.Message, state: FSMContext):
    if message.text:
        data = await state.get_data()
        name = data['name']
        last_name = data['last_name']
        phone = data['phone']
        date = message.text

        user_id = await db.select_user(telegram_id=int(message.from_user.id))
        await db.add_register_info(user_id['id'], name, last_name, phone, date=date)
        await state.finish()
        await message.answer_photo("AgACAgIAAxkBAAIgUGSsMdIyvjkOU5eZl59jfXa_-Gr5AAIKyzEbrclgSWjEkpUIb5i1AQADAgADeQADLwQ", caption="Переходи в меню и знакомься с нашей базой!\n\nОчень рекомендую зайти в \"<b>Домики</b>\" - \"<b>Домик на дереве</b>\" и в \"<b>Развлечения</b>\" - \"<b>Квадроциклы</b>\". Там тебя ждут 🔥 зажигательные 🔥 видеоролики\n\nА так же подпишись на наш основной ТГ канал: @splav40 - там самые актуальные новости и фото.", reply_markup=main_markup)
        await message.answer("На данный момент у тебя есть скидка от 2000 рублей.\n\nЧтобы проверить условия применения и дополнительные бонусы - зайдите в раздел \"АКЦИИ\" или используйте промокод \"Осень23\" при бронировании.")