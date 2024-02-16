from aiogram import F, Router
from aiogram.types import Message


router = Router()


@router.message(F.text == 'special_text')
async def special_text(message: Message):
    await message.reply('special_text')


@router.message(F.text)
async def root(message: Message):
    await message.reply('text')
