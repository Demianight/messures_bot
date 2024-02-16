from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from database.models import Measure, User
from handlers.date import normalize_date

from keyboards.markups import date_markup
from database.crud import create_measure, create_user

router = Router()


class NewMeasure(StatesGroup):
    measure = State()
    date = State()


@router.message(StateFilter(None), Command('new'))
async def retrieve_mesurement(message: Message, state: FSMContext):
    if not message.from_user:
        await message.reply('Что то пошло не так')
        return

    user = User(tg_id=message.from_user.id)

    create_user(user)

    await message.reply(
        'Введите последние измерения.\n'
        'Обязательно соблюдайте формат: X Y\n'
        'Например: 120 80'
    )
    await state.set_state(NewMeasure.measure)


@router.message(
    NewMeasure.measure,
    F.text.regexp(r'\b\d{1,3}\s\d{1,3}\b')
)
async def retrieve_measure(message: Message, state: FSMContext):

    await state.update_data(measure=message.text)

    await message.answer(
        'Супер! Теперь дату измерения.\n'
        'Чтобы выбрать текущую дату можно написать "Сейчас" или нажать на '
        'кнопку клавиатуры бота.\n'
        'Чтобы ввести свою дату укажите ее в формате: чч:мм дд мм гггг\n'
        'Например: 10:30 10 02 2024 (десятое февраля 2024 года в 10:30)\n',
        reply_markup=date_markup()
    )
    await state.set_state(NewMeasure.date)


@router.message(
    NewMeasure.measure
)
async def retrieve_measure_failure(message: Message, state: FSMContext):
    await message.answer(
        'Все таки формат не совпал, проверьте пробелы '
        'и подобные "незаметные" вещи'
    )


@router.message(NewMeasure.date, F.text == 'Сейчас')
async def retrieve_date_now(message: Message, state: FSMContext):
    await state.update_data(date=datetime.now())
    data = await state.get_data()
    await state.clear()

    if not message.from_user:
        await message.reply('Что то пошло не так')
        return

    measure = Measure(**data, user_id=message.from_user.id)
    create_measure(measure)

    await message.reply('Отлично! Все сохранилось')


@router.message(
    NewMeasure.date, F.text.regexp(
        r'\b(?:[01]\d|2[0-3]):(?:[0-5]\d)\s(?:0[1-9]|[12]\d|3[01])\s(?:0[1-9]|1[0-2])\s\d{4}\b'
    )
)
async def retrieve_date_custom(message: Message, state: FSMContext):
    await state.update_data(date=normalize_date(message.text or ''))
    data = await state.get_data()
    await state.clear()

    if not message.from_user:
        await message.reply('Что то пошло не так')
        return

    measure = Measure(**data, user_id=message.from_user.id)
    create_measure(measure)

    await message.reply('Отлично! Все сохранилось')


@router.message(NewMeasure.date)
async def retrieve_date_failure(message: Message, state: FSMContext):
    await message.answer(
        'Попробуй еще раз, по-моему что то не совпало',
        reply_markup=date_markup()
    )
