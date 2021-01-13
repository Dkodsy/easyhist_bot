from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

keyboard_for_admin = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text='Рассылка поста для юзеров'),
                    KeyboardButton(text='Сколько сейчас пользователей?'),

                ],
            ],
            resize_keyboard=True
)

cancel_or_accept = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Одобрить'),
            KeyboardButton(text='⬅️ Отмена')
        ]
    ],
    resize_keyboard=True
)
