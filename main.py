import asyncio
from os import getenv
from pathlib import Path
from typing import NoReturn

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from database.config import create_db
from routers import commands, measure_create, measure_show, messages

GRAPHS_FOLDER = Path('graphs')


async def main() -> NoReturn:

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
