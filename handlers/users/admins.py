from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.admin_keyboard import keyboard
from states.admin_states import Admins
from filters.is_admin import IsAdmin
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
    await message.answer(text='Отвечает сколько пользователей в базе')


@dp.message_handler(state=Admins.enter_text)
async def text_check(message: types.Message):
    text = message.html_text
    await message.answer(f'Проверьте введеный текст(оступы и форматирование сохранено)\n\n'
                         f'{text}', )
    await Admins.check_text.set()


@dp.message_handler(state=Admins.check_text)
async def choose_time(message: types.Message):
    await message.answer()
