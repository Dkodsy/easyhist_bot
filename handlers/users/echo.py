from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    if message.text.lower() == 'вече':
        await message.answer('Ура! Кодовое слово названо верно😉\n'
                             'Держи свой бонус «Ассоциации нашей и всемирной истории» по ссылке ниже»\n\n'
                             'easyhist.ru/bonus\n'
                             'easyhist.ru/bonus\n'
                             'easyhist.ru/bonus')
    elif message.text.lower() == 'барщина':
        await message.answer('Ура! Кодовое слово названо верно😉\n'
                             'Держи свой бонус «Частые ошибки на ЕГЭ»\n\n'
                             'easyhist.ru/secret\n'
                             'easyhist.ru/secret\n'
                             'easyhist.ru/secret')
    else:
        await message.answer('Вероятно, ты хочешь ввести кодовое слово из урока, ты не угадал, попробуй еще раз😊\n'
                             'Если у тебя есть какой-то вопрос, пиши @help_easyhist')


# Эхо хендлер, куда летят ВСЕ сообщения с указанным состоянием
@dp.message_handler(state="*", content_types=types.ContentTypes.ANY)
async def bot_echo_all(message: types.Message):
    await message.answer('Вероятно, ты хочешь ввести кодовое слово из урока, ты не угадал, попробуй еще раз😊\n'
                         'Если у тебя есть какой-то вопрос, пиши @help_easyhist')
