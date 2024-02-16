from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.markups import start_markup


router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        'Welcome to my bot',
        reply_markup=start_markup()
    )
