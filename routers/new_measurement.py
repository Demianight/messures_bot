from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from handlers.date import normalize_date

from keyboards.markups import date_markup

router = Router()


class NewMessure(StatesGroup):
    messure = State()
    date = State()


@router.message(StateFilter(None), Command('new'))
async def add_mesurement(message: Message, state: FSMContext):
    await message.reply(
        'Введите последние измерения.\n'
        'Обязательно соблюдайте формат: X Y\n'
        'Например: 120 80'
    )
    await state.set_state(NewMessure.messure)


@router.message(
    NewMessure.messure,
    F.text.regexp(r'\b\d{1,3}\s\d{1,3}\b')
)
async def add_messure(message: Message, state: FSMContext):
    await state.update_data(messure=list(map(int, message.text.split())))

    await message.answer(
        'Супер! Теперь дату измерения.\n'
        'Чтобы выбрать текущую дату можно написать "Сейчас" или нажать на кнопку клавиатуры бота.\n'
        'Чтобы ввести свою дату укажите ее в формате: чч:мм дд мм гггг\n'
        'Например: 10:30 10 02 2024 (десятое февраля 2024 года в 10:30)\n',
        reply_markup=date_markup()
    )
    await state.set_state(NewMessure.date)


@router.message(
    NewMessure.messure
)
async def add_messure_failure(message: Message, state: FSMContext):
    await message.answer(
        'Все таки формат не совпал, проверьте пробелы '
        'и подобные "незаметные" вещи'
    )


@router.message(NewMessure.date, F.text == 'Сейчас')
async def add_date_now(message: Message, state: FSMContext):
    await state.update_data(date=datetime.now())
    await message.answer(
        str(await state.get_data()),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(
    NewMessure.date, F.text.regexp(
        r'\b(?:[01]\d|2[0-3]):(?:[0-5]\d)\s(?:0[1-9]|[12]\d|3[01])\s(?:0[1-9]|1[0-2])\s\d{4}\b'

    )
)
async def add_date_custom(message: Message, state: FSMContext):
    await state.update_data(date=normalize_date(message.text))
    await message.answer(
        str(await state.get_data()),
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


@router.message(NewMessure.date)
async def add_date_failure(message: Message, state: FSMContext):
    await message.answer(
        'Попробуй еще раз, по-моему что то не совпало',
        reply_markup=date_markup()
    )
