from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Рассылка поста для юзеров'),
                    KeyboardButton(text='Сколько сейчас пользователей?'),

                ],
            ],
            resize_keyboard=True
)
