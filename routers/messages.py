from aiogram import F, Router
from aiogram.types import Message

from answers import MISSED_ANS
from markups import start_markup

router = Router()


@router.message(F.text)
async def root(message: Message):
    await message.reply(
        MISSED_ANS,
        reply_markup=start_markup()
    )
