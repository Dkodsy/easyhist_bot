from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.admin_keyboard import keyboard_for_admin, cancel_or_accept
from states.admin_states import Admins
from filters.is_admin import IsAdmin
from aiogram.utils.markdown import hcode
from loader import dp, db
from utils.mailing import broadcaster


@dp.message_handler(IsAdmin(), Command('admin'))
async def send_to_admin(message: types.Message):
    await message.answer(text='Ку', reply_markup=keyboard_for_admin)


@dp.message_handler(IsAdmin(), text='Рассылка поста для юзеров')
async def enter_text(message: types.Message):
    await message.answer(text='Введите текст поста')
    await Admins.enter_text.set()


@dp.message_handler(IsAdmin(), text='Сколько сейчас пользователей?')
async def enter_text(message: types.Message):
    count_users = await db.count_users()
    await message.answer(text=f'Сейчас пользователей в базе - {count_users}')
    all_users = await db.select_all_users()
    format_all_users = [hcode(user) for user in all_users]
    await message.answer(f'Список пользователей\n{format_all_users}')


@dp.message_handler(state=Admins.enter_text)
async def text_check(message: types.Message, state: FSMContext):
    text = message.html_text
    await state.update_data(post=text)
    await message.answer(f'Проверьте введеный текст(оступы и форматирование сохранено)\n\n'
                         f'{text}', reply_markup=cancel_or_accept)
    await Admins.check_text.set()


@dp.message_handler(state=Admins.check_text, text='Одобрить')
async def choose_time(message: types.Message, state: FSMContext):
    await message.answer('Пост начал отправляться юзерам\n'
                         '(бот будет нагружен в течении небольшого времени(2-5 минут)',
                         reply_markup=keyboard_for_admin)
    data = await state.get_data()
    post = data.get('post')
    await broadcaster(post=post)
    await state.finish()


@dp.message_handler(state=Admins.check_text, text='⬅️ Отмена')
async def choose_time(message: types.Message, state: FSMContext):
    await message.answer('Отмена отправки поста', reply_markup=keyboard_for_admin)
    await state.finish()
