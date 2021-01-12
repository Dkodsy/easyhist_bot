from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from states.admin_states import Admins
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from data import config
from loader import dp, db


@dp.message_handler(Command('admin'))
async def send_to_admin(message: types.Message):
    if str(message.from_user.id) in config.ADMINS:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Добавить пост')
                ],
            ],
            resize_keyboard=True
        )
        await message.answer(text='Ку', reply_markup=keyboard)
    else:
        await message.answer(text='Упс, вы не админ! Напишите @dkodsy, ну или хватит баловаться!')


@dp.message_handler(text='Добавить пост')
async def enter_text(message: types.Message):
    await message.answer(text='Введите текст поста')
    await Admins.enter_text.set()


@dp.message_handler(state=Admins.enter_text)
async def text_check(message: types.Message):
    text = message.html_text
    await message.answer(f'Проверьте введеный текст(оступы и форматирование сохранено)\n\n'
                         f'{text}', )
    await db.add_text(post=text)
    await Admins.check_text.set()


@dp.message_handler(state=Admins.check_text)
async def choose_time(message: types.Message):
    await message.answer()