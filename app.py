from aiogram import executor

from loader import dp, scheduler, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify


async def on_startup(dispatcher):
    # Уведомляет про запуск
    await on_startup_notify(dispatcher)
    await db.create_table_users()


if __name__ == '__main__':
    scheduler.start()
    executor.start_polling(dp, on_startup=on_startup)
