from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.admin_keyboard import keyboard
from states.admin_states import Admins
from filters.is_admin import IsAdmin
from aiogram.utils.markdown import hcode
from loader import dp, db


@dp.message_handler(IsAdmin(), Command('admin'))
async def send_to_admin(message: types.Message):
    await message.answer(text='Ку', reply_markup=keyboard)


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
async def text_check(message: types.Message):
    text = message.html_text
    await message.answer(f'Проверьте введеный текст(оступы и форматирование сохранено)\n\n'
                         f'{text}', )
    await Admins.check_text.set()


@dp.message_handler(state=Admins.check_text)
async def choose_time(message: types.Message):
    await message.answer()
