from aiogram.utils import exceptions
import logging
import asyncio
from loader import dp, db
logging.basicConfig(level=logging.INFO)
log = logging.getLogger('broadcast')


async def get_users():
    user_id = await db.select_all_id()
    return [id[0] for id in user_id]


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    try:
        await dp.bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        logging.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster(post) -> int:
    count = 0
    try:
        for user_id in await get_users():
            if await send_message(user_id, text=post):
                count += 1
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")

    return count

