from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from keyboards.default.main import *
from keyboards.inline.contect_info import admin_markup
from keyboards.inline.check_info import check_markup
from states.getinfo import *


@dp.message_handler(text="🔻Меню", state='*')
async def main_menu(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer_photo("AgACAgIAAxkBAAIC2GSgd4G0D6K2uKmGe4dFLjZNGAZeAALxvjEbXxIJS1e-NrszQ92sAQADAgADeQADLwQ", reply_markup=main_markup)

@dp.message_handler(text="🛎 Забронировать", state='*')
async def do_boron(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Пожалуйста, введите свое полное имя для бронирования: 👇", reply_markup=ReplyKeyboardRemove())
    await message.answer("⬇️")

    await GetInfoBron.full_name.set()

@dp.message_handler(state=GetInfoBron.full_name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    
    await state.update_data({"name":name})
    await message.answer("Введите свой телефон номер: 👇")
    await message.answer("⬇️")

    await GetInfoBron.phone_num.set()

@dp.message_handler(state=GetInfoBron.phone_num)
async def get_phone(message: types.Message, state: FSMContext):
    phone_num = message.text
    
    await state.update_data({"phone_num":phone_num})
    await message.answer("Введите дату, на которую вы хотите забронировать \n\nНапример: 15 Июля 👇", reply_markup=check_date)
    await message.answer("⬇️")

    await GetInfoBron.date.set()

@dp.message_handler(state=GetInfoBron.date)
async def get_date(message: types.Message, state: FSMContext):
    date = message.text
    
    await state.update_data({"date":date})
    await message.answer("Введите количество людей: 👇", reply_markup=ReplyKeyboardRemove())
    await message.answer("⬇️")

    await GetInfoBron.count_perosons.set()

@dp.message_handler(state=GetInfoBron.count_perosons)
async def get_count(message: types.Message, state: FSMContext):
    count_perosons = message.text
    
    await state.update_data({"count_perosons":count_perosons})

    data = await state.get_data()
    name = data['name']
    phone_num = data['phone_num']
    date = data['date']

    await message.answer(f"Проверьте правильность введенных данных:\n\nИмя: {name}\nТелефон номер: {phone_num}\nДата бронирование: {date}\nВсего людей: {count_perosons}", reply_markup=check_markup)

    await GetInfoBron.check.set()

@dp.callback_query_handler(text=['yes', 'no'], state=GetInfoBron.check)
async def cheking(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    name = data['name']
    phone_num = data['phone_num']
    date = data['date']
    count_perosons = data['count_perosons']

    if call.data == 'yes':
        chat_id = '-900586245'

        msg = f"Имя: {name}\nТелефон номер: {phone_num}\nДата бронирование: {date}\nВсего людей: {count_perosons}"
        await bot.send_message(chat_id=chat_id, text=msg)
        
        await state.finish()
        await call.message.answer("Заявка успешно отправлена, скоро с вами свяжутся наши операторы! ✅", reply_markup=main_markup)
        await call.message.answer_photo("AgACAgIAAxkBAAIC2GSgd4G0D6K2uKmGe4dFLjZNGAZeAALxvjEbXxIJS1e-NrszQ92sAQADAgADeQADLwQ")
    else:
        await state.finish()

        await call.message.answer("Заявка на бронирование отменена!", reply_markup=main_markup)
        await call.message.answer_photo("AgACAgIAAxkBAAIC2GSgd4G0D6K2uKmGe4dFLjZNGAZeAALxvjEbXxIJS1e-NrszQ92sAQADAgADeQADLwQ")

@dp.message_handler(text="🔙 Назад", state=GetInfoHoms.home_photos)
@dp.message_handler(text="🏡 Домики", state='*')
async def do_homs(message: types.Message, state: FSMContext):
    await state.finish()
    homs_cat_markup = await creat_homs_markup()
    await message.answer("У нас есть, несколько вариантов размещения: Домик А-фрейм, Домик на Дереве и Высокий А-фрейм. \n\nВ каждом доме есть тёплый пол, кондиционер, крупы и чай каркаде, а так же всё необходимое для проживания:\n\n◽️Большая терраса с 2-мя креслами\n◽️Горячая купель Фурако из лиственницы\n◽️Wifi\n◽️Кухня: электро плита, холодильник, посуда и всё необходимое\n▫️Душевая кабина\n▫️Туалет\n▫️Набор полотенец\n▫️Халаты\n▫️Двухспальный матрас 160 на 200\n▫️Диван\n▫️Мангал и решетка гриль\n▫️В домиках есть все удобства. В них уютно и тепло\n\nНа территории расположены 10 домов разных видов, с минимальным расстоянием друг от друга в 30 метров. Чтобы никто никому не мешал.\n\nВсё передвижение происходит строго с задней стороны домика, по дорожке. Перед домиком и панорамным видом на долину - никто не ходит. \n\n*Все домики оснащены горячей купелью на террасе. \n\nО каком домике хотите узнать подробнее?", reply_markup=homs_cat_markup)
    await GetInfoHoms.home_name.set()

@dp.message_handler(state=GetInfoHoms.home_name)
async def get_name(message: types.Message, state: FSMContext):
    homs = await db.select_all_infomation()

    for home in homs:
        if message.text == str(home['title']):
            photos = home['photos'].split()
            caption = home['caption']
            caption = caption.replace("\\n", '\n')
            await message.answer_photo(photos[0], caption=home['title'], reply_markup=getinfo_markup)
            await message.answer(caption)
            
            await state.update_data({"home_name":message.text})
            await GetInfoHoms.home_photos.set()



@dp.message_handler(text="Смотреть фотографии", state=GetInfoHoms.home_photos)
async def do_home_potos(message: types.Message, state: FSMContext):
    data = await state.get_data()
    home_name = data['home_name']
    homs = await db.select_all_infomation()

    for home in homs:
        if home_name == home['title']:
            photos = home['photos'].split()[1:]
            for photo in photos:
                await message.answer_photo(photo, reply_markup=nav_markup)


@dp.message_handler(text="🥳 Развлечение", state='*')
async def do_raz(message: types.Message, state: FSMContext):
    await state.finish()
    raz_cat_markup = await creat_markup_raz()
    await message.answer("Развлечения на территории глемпинг-парка «НАЗВАНИЕ»\n\n⛱ Зона отдыха у воды с насыпным песком;\n🏐 Волейбольные площадки;\n🌳 Лесные прогулки;\n🎣 Удочки для рыбалки;\n\nА еще👇", reply_markup=raz_cat_markup)
    await GetInfoRaz.raz_name.set()

@dp.message_handler(text="🔙 Назад", state=GetInfoRaz.raz_name)
async def back_5(message: types.Message, state: FSMContext):
    await state.finish()
    raz_cat_markup = await creat_markup_raz()
    await message.answer("Развлечения на территории глемпинг-парка «НАЗВАНИЕ»\n\n⛱ Зона отдыха у воды с насыпным песком;\n🏐 Волейбольные площадки;\n🌳 Лесные прогулки;\n🎣 Удочки для рыбалки;\n\nА еще👇", reply_markup=raz_cat_markup)
    await GetInfoRaz.raz_name.set()

    
@dp.message_handler(state=GetInfoRaz.raz_name)
async def get_raz_name(message: types.Message, state: FSMContext):
    raz_name = message.text
    razs = await db.select_all_infomation2()

    if raz_name:
        for raz in razs:
            if raz_name == raz['title']:
                photo = raz['photos']
                await message.answer_photo(photo, caption=raz['title'], reply_markup=nav_markup)
                await message.answer(raz['caption'])
                

@dp.message_handler(text="🍽 Где поесть", state='*')
async def do_food(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer_photo("AgACAgIAAxkBAAIDCmSggB-Ot7Mk3664bMuxoL0g8wtFAAKu0DEbG8cBSZu0EzNj9qk3AQADAgADeQADLwQ", caption="В каждом шале есть мини кухня. Холодильник, электро плита, чайник, вся необходимая посуда, крупы, чай, кофе. Перед шале мангал, решетка. Можно привезти уголь, розжиг и готовить шашлык. Или по дороге купить готовую еду.\n\nТак же вы можете заказать готовую еду у нас (меню уточняйте у менеджера) 😊", reply_markup=food_cat_markup)

@dp.message_handler(text="🙏 Отзывы", state='*')
async def do_coment(message: types.Message, state: FSMContext):
    await state.finish()
    
    await message.answer("Если вы оставите нам отзыв, мы будем вам очень признательны, только благодаря вам, мы сможем стать лучше 💪", reply_markup=coment_markup)

@dp.message_handler(text="✍️ Написать отзыв", state='*')
async def do_coment(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Ждем ваш отзыв или предложения \n👇", reply_markup=ReplyKeyboardRemove())
    await message.answer("⬇️⁣")

    await GetComent.coment.set()

@dp.message_handler(state=GetComent.coment)
async def get_coment(message: types.Message, state: FSMContext):
    chat_id = '-969985850'

    if message.text:
        msg = f"<b>Имя:</b> {message.from_user.full_name}\n<b>User Name:</b> @{message.from_user.username}\n<b>Telegram ID:</b> {message.from_user.id}\n\n<b>Отзыв:</b> <i>{message.text}</i>"
        await bot.send_message(chat_id=chat_id, text=msg)

        await state.finish()
        await message.answer("🙏 Благодарим вас, мы передадим информацию в службу клиентской заботы", reply_markup=main_markup)
        await message.answer_photo("AgACAgIAAxkBAAIC2GSgd4G0D6K2uKmGe4dFLjZNGAZeAALxvjEbXxIJS1e-NrszQ92sAQADAgADeQADLwQ")

@dp.message_handler(text="📲 Контакты", state='*')
async def do_contact(message: types.Message, state: FSMContext):
    await state.finish()

    await message.answer("Наши контакты\n\nОтдел бронирования\n📲 +7(905)641-84-20\n📲 +7(920)897-05-55\n📩 glamping40@yandex.ru\n🌐 na-krayu-zemli.ru/\n\nГруппа Вконтакте\nhttps://vk.com/splav_na_bajdarkah\n\n📲  +7(905)641-84-20 (телефон администратора \"На краю земли\")\n\n📍Наш адрес: Россия, Панорамная долина, дом 1, Юдинки.", disable_web_page_preview=True, reply_markup=admin_markup)

@dp.message_handler(text="🎉 Акции", state='*')
async def do_aks(message: types.Message, state: FSMContext):
    await state.finish()

    markup = await creat_markup_aks()
    await message.answer("Акции:", reply_markup=markup)
    await GetInfoAks.aks_name.set()

@dp.message_handler(text="🔙 Назад", state=GetInfoAks.aks_name)
async def back_3(message: types.Message, state: FSMContext):
    await state.finish()

    markup = await creat_markup_aks()
    await message.answer("Акции:", reply_markup=markup)
    await GetInfoAks.aks_name.set()


@dp.message_handler(state=GetInfoAks.aks_name)
async def do_aks(message: types.Message, state: FSMContext):
    aks = message.text 
    if aks:
        aksiyi = await db.select_all_infomation3()
        for aksya in aksiyi:
            if aks == aksya['title']:
                await message.answer(aksya['caption'], reply_markup=nav_markup)
                break