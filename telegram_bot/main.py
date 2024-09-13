import asyncio
import logging

from aiogram import Bot, Dispatcher
# from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from handlers import router
from admin import secret_token

from dotenv import load_dotenv

load_dotenv()

# bot = Bot(token=secret_token)


async def main():
    bot = Bot(token=secret_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
