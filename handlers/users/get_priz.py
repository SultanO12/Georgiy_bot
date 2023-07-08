from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from states.getinfo import GetRegInfo
from keyboards.default.main import *

@dp.message_handler(text="🎁 Получить подарок", state='*')
async def get_reg_info(message: types.Message, state: FSMContext):
    await state.finish()

    user = await db.select_user(telegram_id=message.from_user.id)
    reg_user = await db.select_register_info(user_id=int(user['id']))

    if reg_user is None:
      await message.answer("🖐 Как тебя зовут?")
      await message.answer("⬇️")

      await GetRegInfo.first_name.set()

@dp.message_handler(state=GetRegInfo.first_name)
async def get_name(message: types.Message, state: FSMContext):
    if message.text:
      name = message.text
      
      await state.update_data({"name":name})
      await message.answer(f"🙌 {name}, очень приятно познакомиться с тобой!")
      await message.answer(f"У меня уже есть друг {name}, чтобы мне вас не перепутать, напиши свою фамилию")
      await message.answer("⬇️")

      await GetRegInfo.last_name.set()

@dp.message_handler(state=GetRegInfo.last_name)
async def get_last_name(message: types.Message, state: FSMContext):
    if message.text:
        last_name = message.text
        data = await state.get_data()
        name = data['name']

        await state.update_data({"last_name":last_name})
        await message.answer(f"{name}, у меня последний вопрос!\n\nНапиши свой телефон, что бы наш администратор ничего не перепутала, а то она может )", reply_markup=send_number_markup)
        await message.answer("⬇️")

        await GetRegInfo.phone.set()

@dp.message_handler(state=GetRegInfo.phone)
async def get_phone(message: types.Message, state: FSMContext):
    if message.text:
        phone = message.text
        data = await state.get_data()
        name = data['name']
        last_name = data['last_name']

        user_id = await db.select_user(telegram_id=int(message.from_user.id))
        await db.add_register_info(user_id['id'], name, last_name, phone)

        await message.answer("😍 Отлично!\n\n💖 Теперь мы стали ближе", reply_markup=main_markup)
        await message.answer(f"{name}, на ваш бонусный счет зачислено 1000 ₽. \n\nТы можешь ими воспользоваться у нас глэмпинг-парке, при бронировании домиков или дополнительных услуг")
        
        await state.finish()