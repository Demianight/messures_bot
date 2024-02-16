import asyncio
from os import getenv
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher

from routers import commands, messages, new_measurement


async def main() -> None:
    load_dotenv()

    token = getenv('TG_TOKEN')

    bot = Bot(token)
    dp = Dispatcher()

    dp.include_router(new_measurement.router)
    dp.include_router(commands.router)
    dp.include_router(messages.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
