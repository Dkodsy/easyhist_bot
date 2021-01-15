import asyncpg
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import datetime, timedelta

from loader import dp, scheduler, db

video = 'BAACAgIAAxkBAAMIYAHDRdnyxDD_O3syTxgf-i6lguoAAtYLAALSp_lLI1JkFh23i7UeBA'
photo_1 = 'AgACAgIAAxkBAAMKYAHDd5N_nSsQ7zzVVnAM4uoMFNcAAi6xMRtQeRFIWMIGHltEi1lMwimbLgADAQADAgADeQADCFsBAAEeBA'
file_message_four = 'BQACAgIAAxkBAAMOYAHD2RT_PdTpr9kDiAsT0EEDyH8AAnYKAAJQeRFIskgmVHTMtoseBA'
photo_message_four = 'AgACAgIAAxkBAAMMYAHDtS-_KOa0hbxywjbLsx6-rHUAAi-xMRtQeRFIPVpNbKLGjVBO6xeYLgADAQADAgADeQADybIFAAEeBA'


@dp.message_handler(CommandStart())
async def message_one(message: types.Message):
    await message.answer_video(
        video=video,
        caption="Привет👋🏻 Включи звук")
    user_id = message.from_user.id

    try:
        await db.add_user(id=user_id,
                          name=message.from_user.full_name,
                          start_time=datetime.now())
    except asyncpg.exceptions.UniqueViolationError as err:
        print("Пользователь уже в базе\n", err)
        return None

    start_time = await db.select_start_time(id=user_id)

    async def message_two(message: types.message):
        await message.answer(text="✅ Поздравляю, регистрация прошла успешно!\n\n"
                                  "Ты находишься в основном канале интенсива «Древняя Русь за 5 дней»‎,"
                                  "где будут публиковаться ссылки на доступ к урокам, важные новости и вся "
                                  "наша с тобой связь!\n\n"
                                  "📅 <b>Даты интенсива:</b> 18 — 22 января\n\n"
                                  "Уроки будут выходить на специальной платформе, ссылку на неё пришлю позже.\n\n"
                                  "Как только выйдет первый урок, я напомню тебе, а пока смотри программу, которую мы "
                                  "приготовили👇🏻\n\n"
                                  "📑 Программа интенсива:\n\n"
                                  "1️⃣ 18 января 15:00 МСК (Урок 1)\n\n"
                                  "<b>Кто такие восточные славяне?</b>\n\n"
                                  "— Изучим народы и древнейшие государства на территории России\n "
                                  "— Чем занимались, как жили, во что верили восточные славяне?\n"
                                  "— Обсудим возникновение государства\n\n"
                                  "2️⃣ 20 января 15:00 МСК (Урок 2)\n\n"
                                  "<b>Первые Рюриковичи</b>\n\n"
                                  "— Рассмотрим деятельность первых князей\n"
                                  "— Проследим тонкости принятия христианства\n"
                                  "— Поговорим о  Русской Правде\n"
                                  "— Исследуем международные связи Древней Руси\n\n"
                                  "3️⃣ 22 января 15:00 МСК (Урок 3)\n\n"
                                  "<b>Раздробленность и борьба крупнейших княжеств</b>\n\n"
                                  "— Разберём русскую Игру престолов\n"
                                  "— Выясним почему поссорились русские князья\n"
                                  "— Выделим основные княжества\n")
        await message.answer_photo(photo=photo_1)

    async def message_three(message: types.Message):
        await message.answer(text='<b>Правила и нюансы интенсива:</b>\n\n'
                                  '📹 <b>Уроки в записи.</b>\n\n'
                                  'Из-за неудобного графика или работы не всегда удается попасть '
                                  'на живую трансляцию — мы заранее отсняли уроки, чтобы ты мог посмотреть '
                                  'их в любое время: за завтраком, после учебы или ночью.\n\n'
                                  'Уроки будут выходить в понедельник, среду и пятницу в 15:00 по Москве.\n\n'
                                  '⏰ <b>Уроки доступны не навсегда.</b>\n\n'
                                  'Я за то, чтобы пользоваться возможностями сразу и не откладывать — '
                                  'любителям «начинать с понедельника» точно не подойдёт.\n\n'
                                  'Я предупрежу заранее, когда будем закрывать доступ, '
                                  'но советую смотреть уроки сразу, как они выходят.\n\n'
                                  '📓 <b>Секретные бонусы за просмотр уроков.</b>\n\n'
                                  'Вводи кодовые слова, которые я называю на каждом уроке и получай бонусные материалы.'
                                  '\n\n'
                                  'С ними ты ускоришь своё обучение и сможешь подготовиться к '
                                  'ЕГЭ на 80+ всего за 4 месяца.\n\n'
                                  'Бонусы выдаются только в первые 24 часа после выхода урока — как их забрать, '
                                  'расскажу завтра.\n\n'
                                  '📝 <b>Домашние задания.</b>\n\n'
                                  'По итогу интенсива ты получишь знания, которые в школе проходят несколько месяцев. '
                                  'Согласись, звучит круто?\n\n'
                                  'Чтобы воспользоваться ими на ЕГЭ, нужно:\n\n'
                                  '— Полностью посмотреть все уроки\n'
                                  '— Выполнить 3 домашних задания')

    async def message_four(message: types.Message):
        await message.answer_photo(photo=photo_message_four,
                                   caption='Чтобы ты дошел до конца, по пути мы разложили 3 бонуса: '
                                           'забирай первый по ссылке ниже — справочник «Архитектура Древней Руси»\n'
                                           'А через час я пришлю тебе инструкцию как получить остальные бонусы.')
        await message.answer_document(document=file_message_four)

    async def message_five(message: types.Message):
        await message.answer(
            text='И спасибо тебе огромное за доверие! 😌🙏🏻\n\n'
                 'Ты даже не представляешь, насколько для меня ценно, '
                 'что ты принял участие в интенсиве.\n\n'
                 'Так хочется, чтобы ты поскорее это увидел, просто не терпится открыть '
                 'доступ к первому уроку!\n\n'
                 'Мы с командой выложились на 1000%, чтобы за следующую неделю максимально '
                 'прокачать твои знания в этой теме и помочь сдать ЕГЭ по истории на 80+ баллов.\n\n'
                 'Чего говорить, ты сам всё увидишь уже 18 января 😏\n\n'
                 '📩 Если у тебя появился любой вопрос по интенсиву, смело пиши в техподдержку @help_easyhist\n\n'
                 '☝🏻 Ребята отвечают оперативно, чтобы ни один вопрос не остался без ответа')

    async def message_six(message: types.Message):
        await message.answer(
            text='📑 <b>Инструкция: как получать секретные бонусы за просмотр уроков.</b>\n\n'
                 'В видео выше рассказал, что в 1 и 2 уроке '
                 'спрятаны слова, которые открывают доступ к  дополнительным материалам.\n\n'
                 '📔 Например, на первом уроке тебя ждёт файл «Ассоциации нашей и всемирной истории»\n\n'
                 'С ним ты:\n\n'
                 '— Поможет тебе не потерять баллы в 1 и 11 заданиях\n'
                 '— Позволит тебе не терять время на запоминание всей зарубежной истории\n\n'
                 '<b>Теперь рассказываю, как его получить:</b>\n\n'
                 '1. Найти кодовое слово в уроке — я сделаю на нём акцент, чтобы ты его не упустил\n\n'
                 '2. Отправь в этот диалог кодовое слово в первые 24 часа после выхода урока\n\n'
                 '3. Бонус сразу придёт тебе обратным сообщением\n\n'
                 '—————\n\n'
                 '<b>Все просто:</b> 18 января в 15:00 выходит урок, смотришь, находишь слово, вводишь в бот, '
                 'забираешь бонус\n\nТак же на втором уроке — всего будет 2 слова, которые сложатся в особую фразу')

    scheduler.add_job(message_two, 'date', run_date=start_time + timedelta(seconds=60), args=(message,))
    scheduler.add_job(message_three, 'date', run_date=start_time + timedelta(seconds=120), args=(message,))
    scheduler.add_job(message_four, 'date', run_date=start_time + timedelta(seconds=180), args=(message,))
    scheduler.add_job(message_five, 'date', run_date=start_time + timedelta(seconds=240), args=(message,))
    scheduler.add_job(message_six, 'date', run_date=start_time + timedelta(seconds=3600), args=(message,))
