from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message

from database.crud import get_measures, _get_measures
from handlers.graph import create_graph

router = Router()


@router.message(StateFilter(None), Command('show_raw'))
async def show_measures(message: Message):
    if not message.from_user:
        await message.reply('Что то пошло не так')
        return

    measures = str(get_measures(message.from_user.id))

    await message.reply(measures)


@router.message(StateFilter(None), Command('show'))
async def retrieve_mesurement(message: Message):
    if not message.from_user:
        await message.reply('Что то пошло не так')
        return

    create_graph(_get_measures(message.from_user.id))
