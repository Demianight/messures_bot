from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from answers import HELP_ANS, MAIN_ANS
from markups import start_markup

router = Router()


@router.message(Command('start'))
async def start(message: Message):
    await message.answer(
        MAIN_ANS,
        reply_markup=start_markup()
    )


@router.message(Command('help'))
async def help(message: Message):
    await message.answer(
        HELP_ANS,
        reply_markup=start_markup()
    )
