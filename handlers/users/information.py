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
    await message.answer_photo(photo='AgACAgIAAxkBAAIQv2Sm2jXX01WJObT-ZbxYCN9GhT7wAAJfzTEbLZAxSQpsKz38nkgfAQADAgADeQADLwQ', caption="На территории расположены 10 домов разных видов, с минимальным расстоянием друг от друга в 30 метров. Чтобы никто никому не мешал.\n\nВсё передвижение происходит строго с задней стороны домика, по дорожке. Перед домиком и панорамным видом на долину - никто не ходит. \n\nУ нас есть, несколько вариантов размещения: Домик А-фрейм, Домик на Дереве и Высокий А-фрейм. \n\nВ каждом доме есть тёплый пол, кондиционер, крупы и чай каркаде, а так же всё необходимое для проживания:\n\n◽️Большая терраса с 2-мя креслами\n◽️Горячая купель Фурако из лиственницы\n▫️Кондиционер\n▫️Теплый пол\n◽️Wifi\n◽️Кухня: электро плита, холодильник, посуда и всё необходимое\n▫️Душевая кабина\n▫️Туалет\n▫️Набор полотенец\n▫️Халаты\n▫️Двухспальный матрас 160 на 200\n▫️Диван\n▫️Мангал и решетка гриль\n▫️В домиках есть все удобства. В них уютно и тепло\n\n*Все домики оснащены горячей купелью на террасе. \n\nО каком домике хотите узнать подробнее?", reply_markup=homs_cat_markup)
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
            if home['video']:
                videos = home['video'].split()
                for video in videos:
                    await message.answer_video(video, reply_markup=nav_markup)


@dp.message_handler(text="🥳 Развлечение", state='*')
async def do_raz(message: types.Message, state: FSMContext):
    await state.finish()
    raz_cat_markup = await creat_markup_raz()

    photo1 = 'https://i.ibb.co/xsYV6qv/image.png'
    photo2 = 'https://i.ibb.co/LdWN262/image.png'
    photo3 = 'https://i.ibb.co/0X1JgZR/image.png'

    media = types.MediaGroup()
    media.attach_photo(photo=photo1)
    media.attach_photo(photo=photo2, caption='У нас есть два варианта развлечений:\n\n1) Прогулка на квадроциклах (работает круглый год, независимо от сезона)\n\n2) Сплав на байдарках (Работает с мая по октябрь, пока позволяет погода)\n\nПро что рассказать подробнее?')
    media.attach_photo(photo=photo3)
    await message.answer_media_group(media)
    await message.answer("💬⁣", reply_markup=raz_cat_markup)
    await GetInfoRaz.raz_name.set()

@dp.message_handler(text="🔙 Назад", state=GetInfoRaz.raz_photo_cvad)
async def back_5(message: types.Message, state: FSMContext):
    await state.finish()
    raz_cat_markup = await creat_markup_raz()

    photo1 = 'https://i.ibb.co/xsYV6qv/image.png'
    photo2 = 'https://i.ibb.co/LdWN262/image.png'
    photo3 = 'https://i.ibb.co/0X1JgZR/image.png'

    media = types.MediaGroup()
    media.attach_photo(photo=photo1)
    media.attach_photo(photo=photo2, caption='У нас есть два варианта развлечений:\n\n1) Прогулка на квадроциклах (работает круглый год, независимо от сезона)\n\n2) Сплав на байдарках (Работает с мая по октябрь, пока позволяет погода)\n\nПро что рассказать подробнее?')
    media.attach_photo(photo=photo3)
    await message.answer_media_group(media)
    await message.answer("💬⁣", reply_markup=raz_cat_markup)
    await GetInfoRaz.raz_name.set()


    
@dp.message_handler(state=GetInfoRaz.raz_name)
async def get_raz_name(message: types.Message, state: FSMContext):
    raz_name = message.text

    if raz_name:
        if raz_name == "КВАДРОЦИКЛЫ":
            photo = 'AgACAgIAAxkBAAIRQGSm7mZgsmc86kNv5QgDoSpMCL05AAK8zTEbLZAxSRRlnV6mSceuAQADAgADeQADLwQ'
            await message.answer_photo(photo, caption="Стоимость погулки: 8,500 руб - 2-х часовая программа для двоих человек на 2-х местном квадрике\n\n🔥В стоимость входит:\n\n✅ Инструктаж и пробный заезд\n✅ Сопровождение инструктора и помощь на всем пути\n✅ Авторский драйвовый подготовленный лесной маршрут\n✅ Фото-видео во время мероприятия на iphone 13 pro\n✅ Шлем\n✅ ГСМ\n\nЕсть 3 варианта сложности прохождения маршрута: легкий / средний  и ЭКСТРИМ. На предварительном прокате решаем вместе, по какому поедем. Всегда сложность можно изменить.\n\nПри этом можно много чего совместить:\n- покататься 2 часа на свежем воздухе\n- насладиться красотой природы\n- промчаться с ветерком\n- получить большое количество положительных эмоций\n- Пересечь водоём 😃\n- и ещё огромный заряд энергии и адреналин 🔥", reply_markup=photos_markup)
            await GetInfoRaz.raz_photo_cvad.set()
    elif raz_name == "Сплавы на байдарках":
        photo = 'AgACAgIAAxkBAAISBGSoIKYEDWQdyZmflhXXHoP-iq10AAIWyjEbqDNAScOnXIF3wsjcAQADAgADeQADLwQ'
        await message.answer_photo(photo, caption='Сплавы на байдарках организовываются на реке Серёна, Калужская область Козельский район.\n\n❤️‍🔥 (Более 1000 отзывов по хэштгу #splav40 в запрещеной соц. сети) 🤟\n\nРека очень живописная и интересная. Постоянно меняется картинка, пейзажи.\n\nМестами сужается - увеличивается скорость течения\nМестами широкая, как озеро. Очень интересно.\nРечка не широкая, поэтому деревья наклоняются прямо над водой.\n\nЕсть на пути преграды, которые создают динамичность маршруту. Очень интересно!\n\nЕсть однодневные сплавы, а есть двухдневные. Про какие рассказать подробнее? \n\nВАРИАНТЫ ОТВЕТОВ: Однодневный сплав ! Двухдневный сплав  ! Меню', reply_markup=splavs_markup)
        await GetInfoRaz.raz_cat_splav.set()

@dp.message_handler(text="🔙 Назад", state=GetInfoRaz.raz_cat_splav)
async def back_5(message: types.Message, state: FSMContext):
    photo = 'AgACAgIAAxkBAAISBGSoIKYEDWQdyZmflhXXHoP-iq10AAIWyjEbqDNAScOnXIF3wsjcAQADAgADeQADLwQ'
    await message.answer_photo(photo, caption='Сплавы на байдарках организовываются на реке Серёна, Калужская область Козельский район.\n\n❤️‍🔥 (Более 1000 отзывов по хэштгу #splav40 в запрещеной соц. сети) 🤟\n\nРека очень живописная и интересная. Постоянно меняется картинка, пейзажи.\n\nМестами сужается - увеличивается скорость течения\nМестами широкая, как озеро. Очень интересно.\nРечка не широкая, поэтому деревья наклоняются прямо над водой.\n\nЕсть на пути преграды, которые создают динамичность маршруту. Очень интересно!\n\nЕсть однодневные сплавы, а есть двухдневные. Про какие рассказать подробнее? \n\nВАРИАНТЫ ОТВЕТОВ: Однодневный сплав ! Двухдневный сплав  ! Меню', reply_markup=splavs_markup)
    await GetInfoRaz.raz_cat_splav.set()

@dp.message_handler(state=GetInfoRaz.raz_cat_splav)
async def get_splav_name(message: types.Message, state: FSMContext):
    splav = message.text

    if splav:
        if splav == 'Однодневный сплав':
            await state.update_data({"splav_id":1})
            await state.update_data({"splav_name":splav})
            photo = 'AgACAgIAAxkBAAISQmSoJ79dGEYJ1m2lZutQ3tO7lTVVAAJqyjEbqDNASYa84zHKltgXAQADAgADeQADLwQ'
            await message.answer_photo(photo, caption="Ответ:\n\n✅ Однодневные:\n\nЧто входит в 1-дневный сплав:\n\n• Трансфер из Калуги, Козельска, шале до старта и обратно (по выходным)\n• Все снаряжение для сплава, инструктаж, сопровождение\n• Питание 1 раз, полевая кухня на костре\n• Отдых на организованной базе: волейбольная сетка, настольный теннис. \n🔥 Хорошее настроение, море эмоций и настоящая перезагрузка! \n(Более 1000 отзывов по хэштгу #splav40 в запрещеной соц. сети)\n\nСтоимость:\nСплав 1 дневный в будни - 4000 руб\n(3400 дети до 14)\nСплав 1 дневный в выходные - 4500 руб\n(3800 дети до 14)", reply_markup=nav_spav_markup)
            await GetInfoRaz.raz_photo_splav.set()
            
        elif splav == 'Двухдневные сплавы':
            photo = 'AgACAgIAAxkBAAISQGSoJ64-9U7JNZoVM3Pxf8jR4_1zAAIWyjEbqDNAScOnXIF3wsjcAQADAgADeQADLwQ'
            await message.answer_photo(photo, caption="ОТВЕТ:\n\n✅ Что входит в 2-дневный сплав:\n\n•  Трансфер из Калуги и обратно\n• Все снаряжение, инструктаж, сопровождение\n• Живописный авторский подготовленный маршрут\n• Фото мероприятия\n•Походная баня на берегу реки\n• Питание 5 раз (3 раза в первый день, и 2 раза во второй), полевая кухня на костре, готовим еду ресторанного качества казане и на мангале\n• Палатки и спальники предоставляем.\n• Машина сопровождения (вещи отдельно едут в машине, а мы сплавляемся налегке)\n🔥 Хорошее настроение, море эмоций и настоящая перезагрузка! \n(Более 1000 отзывов по хэштгу #splav40 в запрещеной соц. сети подтверждают это!)\n\nА так же с нами постоянно компании: Альфа-банк, Volkswagen group, Россельхозбанк и другие! \n\nЦена:\n\nСплав 2 дневный со своими палатками 10500 (вых и будни)\n(8900 дети до 14)\nСплав 2 дневный с нашими палатками 12000 (вых и будни)\n(10200 дети до 14)")
            await state.update_data({"splav_id":2})
            await state.update_data({"splav_name":splav})
            await GetInfoRaz.raz_photo_splav.set()

@dp.message_handler(text="🔙 Назад", state=GetInfoRaz.raz_photo_splav)
async def back_5(message: types.Message, state: FSMContext):
    data = await state.get_data()
    splav = data['splav_name']

    if splav:
        if splav == 'Однодневный сплав':
            await state.update_data({"splav_id":1})
            await state.update_data({"splav_name":splav})
            photo = 'AgACAgIAAxkBAAISQmSoJ79dGEYJ1m2lZutQ3tO7lTVVAAJqyjEbqDNASYa84zHKltgXAQADAgADeQADLwQ'
            await message.answer_photo(photo, caption="Ответ:\n\n✅ Однодневные:\n\nЧто входит в 1-дневный сплав:\n\n• Трансфер из Калуги, Козельска, шале до старта и обратно (по выходным)\n• Все снаряжение для сплава, инструктаж, сопровождение\n• Питание 1 раз, полевая кухня на костре\n• Отдых на организованной базе: волейбольная сетка, настольный теннис. \n🔥 Хорошее настроение, море эмоций и настоящая перезагрузка! \n(Более 1000 отзывов по хэштгу #splav40 в запрещеной соц. сети)\n\nСтоимость:\nСплав 1 дневный в будни - 4000 руб\n(3400 дети до 14)\nСплав 1 дневный в выходные - 4500 руб\n(3800 дети до 14)", reply_markup=nav_spav_markup)
            await GetInfoRaz.raz_photo_splav.set()
            
        elif splav == 'Двухдневные сплавы':
            photo = 'AgACAgIAAxkBAAISQGSoJ64-9U7JNZoVM3Pxf8jR4_1zAAIWyjEbqDNAScOnXIF3wsjcAQADAgADeQADLwQ'
            await message.answer_photo(photo, caption="ОТВЕТ:\n\n✅ Что входит в 2-дневный сплав:\n\n•  Трансфер из Калуги и обратно\n• Все снаряжение, инструктаж, сопровождение\n• Живописный авторский подготовленный маршрут\n• Фото мероприятия\n•Походная баня на берегу реки\n• Питание 5 раз (3 раза в первый день, и 2 раза во второй), полевая кухня на костре, готовим еду ресторанного качества казане и на мангале\n• Палатки и спальники предоставляем.\n• Машина сопровождения (вещи отдельно едут в машине, а мы сплавляемся налегке)\n🔥 Хорошее настроение, море эмоций и настоящая перезагрузка! \n(Более 1000 отзывов по хэштгу #splav40 в запрещеной соц. сети подтверждают это!)\n\nА так же с нами постоянно компании: Альфа-банк, Volkswagen group, Россельхозбанк и другие! \n\nЦена:\n\nСплав 2 дневный со своими палатками 10500 (вых и будни)\n(8900 дети до 14)\nСплав 2 дневный с нашими палатками 12000 (вых и будни)\n(10200 дети до 14)")
            await state.update_data({"splav_id":2})
            await state.update_data({"splav_name":splav})
            await GetInfoRaz.raz_photo_splav.set()

@dp.message_handler(text="Смотреть фотографии" , state=GetInfoRaz.raz_photo_splav)
async def send_photos_splav(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data['splav_id'] == 1:
        photos = ['AgACAgIAAxkBAAISOmSoJ5vIjRouSti98T5gI2NdYOD-AAJgyjEbqDNASQVZOmmxuML-AQADAgADeQADLwQ', 'AgACAgIAAxkBAAISPGSoJ6JZC3zd0XP71gjMhfUZUKMdAAJhyjEbqDNASZXzreF3EKzIAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISPmSoJ6jR0WIkpjlUnjqFI9-64erVAAJjyjEbqDNASfXnS3Fse4_NAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISQGSoJ64-9U7JNZoVM3Pxf8jR4_1zAAIWyjEbqDNAScOnXIF3wsjcAQADAgADeQADLwQ']

        for photo in photos:
            await message.answer_photo(photo, reply_markup=nav_markup)
    if data['splav_id'] == 2:
        photos = ['AgACAgIAAxkBAAISUWSoKQemTbuqF2txYIN2e4lyrGZHAAJ0yjEbqDNASdtw9E29xZNtAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISU2SoKQdgKSlB8Hnn58baGDVo3CV9AAJ2yjEbqDNASdIcwASZ6aDMAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISVmSoKQf7XWPkA8wROT36W-_0mPLtAAIFyTEbwbk4ScWJ3Dun8m9zAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISVGSoKQefbbd3fIeo5Mjx5dvirLixAAIDyTEbwbk4SWn__w3LeHvSAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISVWSoKQd59FsTBZldEfX0BB0aTSSJAAIEyTEbwbk4SfEXEUJIpqeCAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISV2SoKQeYh0NqVyHA5j7ri0UynsSNAAIGyTEbwbk4SV4dh7pH1uU7AQADAgADeQADLwQ', 'AgACAgIAAxkBAAISWWSoKQfxT9X6L8mRedH_U1C5z_suAAIIyTEbwbk4ScUAAafF3oJSGAEAAwIAA3kAAy8E', 'AgACAgIAAxkBAAISWGSoKQemrSGoQYQtkh7_a4z9-fsyAAIHyTEbwbk4SVHRLW2WCz8mAQADAgADeQADLwQ', 'AgACAgIAAxkBAAISUmSoKQeZpzxxHX4PAvZ2PR9MyAABXwACdcoxG6gzQElKpxRT3SxJwwEAAwIAA3kAAy8E']

        for photo in photos:
            await message.answer_photo(photo, reply_markup=nav_markup)

@dp.message_handler(text="Смотреть фотографии", state=GetInfoRaz.raz_photo_cvad)
async def send_photos_cvad(message: types.Message, state: FSMContext):
    photos = ['AgACAgIAAxkBAAIRVmSm-JYP0XAHwpxDHM-xufHU7IPJAAIezjEbLZAxSUS6NGsl2QsIAQADAgADeAADLwQ', 'AgACAgIAAxkBAAIRV2Sm-JY2biqmlklxlUTusbK6-2vQAAIfzjEbLZAxSQ1Kf_PbVZekAQADAgADeQADLwQ', 'AgACAgIAAxkBAAIRWGSm-JYWZ_FynivvgwKnpgaUR8c4AAK8zTEbLZAxSRRlnV6mSceuAQADAgADeQADLwQ', 'AgACAgIAAxkBAAIRWWSm-JbtDiKC_HjoPjDr0S08Zy0yAAIgzjEbLZAxSfNBkUKJmO0GAQADAgADeQADLwQ']
    videos = ['BAACAgIAAxkBAAIRamSm-47ISfXaW33J9I7-cOcbGtZOAAKuKwACD2vBSNWlieHMb0ZTLwQ', 'BAACAgIAAxkBAAIRaGSm-4G440mcdHkyZMsvHKNhgVj9AAIDNAACLZAxSblJwsAH6n0WLwQ']
    for photo in photos:
        await message.answer_photo(photo, reply_markup=nav_markup)
    for video in videos:
        await message.answer_video(video, reply_markup=nav_markup)
        
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

    await message.answer("Наши контакты\n\nОтдел бронирования\n📲 +7(920)897-05-55\n📲 +7(905)641-84-20\n🌐 Сайт:  na-krayu-zemli.ru/\n\nГруппа Вконтакте\nhttps://vk.com/splav_na_bajdarkah\n\n📲  +7(905)641-84-20 (телефон администратора \"На краю земли\")\n\n📍Наш адрес: Россия, Калужская область, Козельский район,  ул. Панорамная долина, дом 1, Юдинки.", disable_web_page_preview=True, reply_markup=admin_markup)

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