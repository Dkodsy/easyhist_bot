import asyncpg
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.builtin import CommandStart
from datetime import datetime, timedelta

from loader import dp, scheduler, db


@dp.message_handler(CommandStart())
async def start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    user_id = message.from_user.id

    try:
        await db.add_user(id=user_id,
                          name=message.from_user.full_name,
                          start_time=datetime.now())
    except asyncpg.exceptions.UniqueViolationError as err:
        print("Пользователь уже в базе\n", err)

    start_time = await db.select_start_time(id=user_id)

    async def send_with_timer_1(dp: Dispatcher):
        await dp.bot.send_message(user_id,
                                  text="Текст, ссылка, какая нибудь хуйня")

    async def send_with_timer_2(dp: Dispatcher):
        await dp.bot.send_message(user_id,
                                  text="Текст, ссылка, какая нибудь хуйня (2)")

    async def send_with_timer_3(dp: Dispatcher):
        await dp.bot.send_message(user_id,
                                  text="Текст, ссылка, какая нибудь хуйня (3)")

    scheduler.add_job(send_with_timer_1, 'date', run_date=start_time + timedelta(seconds=10), args=(dp,))
    scheduler.add_job(send_with_timer_2, 'date', run_date=start_time + timedelta(seconds=60), args=(dp,))
    scheduler.add_job(send_with_timer_3, 'date', run_date=start_time + timedelta(seconds=65), args=(dp,))

