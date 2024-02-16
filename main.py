import asyncio
from os import getenv
from database.config import create_db
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from routers import commands, messages, measure_create, measure_show


async def main() -> None:

    create_db()

    load_dotenv()

    token: str = getenv('TG_TOKEN') or ''

    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(measure_create.router)
    dp.include_router(measure_show.router)
    dp.include_router(commands.router)
    dp.include_router(messages.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
