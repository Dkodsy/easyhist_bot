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


@dp.message_handler(IsAdmin(), text='Сколько сейчас пользователей?')
async def enter_text(message: types.Message):
    count_users = await db.count_users()
    await message.answer(text=f'Сейчас пользователей в базе - {count_users}')
    all_users = await db.select_all_users()
    format_all_users = []
    for user in all_users:
        user = f'id - {user[0]}, name-{user[1]}, Время нажатия на старт - {user[2]}\n'
        format_all_users.append(user)
    print(format_all_users)
    await message.answer(f"Список пользователей\n{''.join(format_all_users)}")


@dp.message_handler(IsAdmin(), text='Рассылка поста для юзеров')
async def enter_text(message: types.Message):
    await message.answer(text='Введите текст поста')
    await Admins.enter_text.set()


@dp.message_handler(state=Admins.enter_text, content_types=types.ContentTypes.VIDEO)
async def text_check(message: types.Message, state: FSMContext):
    video_id = message.video.file_id
    caption = message.caption
    await state.update_data(video=video_id)
    await state.update_data(caption=caption)
    await message.answer(f'Проверьте введенное сообщение(оступы и форматирование сохранено)\n\n',
                         reply_markup=cancel_or_accept)
    await message.answer_video(video_id, caption=caption)
    await Admins.check_text.set()


@dp.message_handler(state=Admins.enter_text, content_types=types.ContentTypes.PHOTO)
async def text_check(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    caption = message.caption
    await state.update_data(photo=photo_id)
    await state.update_data(caption=caption)
    await message.answer(f'Проверьте введенное сообщение(оступы и форматирование сохранено)\n\n',
                         reply_markup=cancel_or_accept)
    await message.answer_photo(photo_id, caption=caption)
    await Admins.check_text.set()


@dp.message_handler(state=Admins.enter_text, content_types=types.ContentTypes.DOCUMENT)
async def text_check(message: types.Message, state: FSMContext):
    file_id = message.document.file_id
    caption = message.caption
    await state.update_data(file=file_id)
    await state.update_data(caption=caption)
    await message.answer(f'Проверьте введенное сообщение(оступы и форматирование сохранено)\n\n',
                         reply_markup=cancel_or_accept)
    await message.answer_document(file_id, caption=caption)
    await Admins.check_text.set()


@dp.message_handler(state=Admins.enter_text, content_types=types.ContentTypes.TEXT)
async def text_check(message: types.Message, state: FSMContext):
    text = message.html_text
    await state.update_data(post=text)
    await message.answer(f'Проверьте введенное сообщение(оступы и форматирование сохранено)\n\n'
                         f'{text}', reply_markup=cancel_or_accept)
    await Admins.check_text.set()


@dp.message_handler(state=Admins.check_text, text='Одобрить')
async def choose_time(message: types.Message, state: FSMContext):
    await message.answer('Начал отправку',
                         reply_markup=keyboard_for_admin)
    data = await state.get_data()
    post = data.get('post')
    photo = data.get('photo')
    caption = data.get('caption')
    video = data.get('video')
    file = data.get('file')
    count = await broadcaster(post=post, photo=photo, video=video, caption=caption, file=file)
    await message.answer(f'<b>{count}</b> messages successful sent.')
    await state.finish()


@dp.message_handler(IsAdmin(), state='*', text='⬅️ Отмена')
async def choose_time(message: types.Message, state: FSMContext):
    await message.answer('Отмена отправки поста', reply_markup=keyboard_for_admin)
    await state.finish()
