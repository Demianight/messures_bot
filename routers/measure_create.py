from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message

from answers import (CONGRATS_ANS, DATE_CHOICE_ANS, DATE_DAY_ANS,
                     DATE_FAILURE_ANS, DATE_HOUR_ANS, DATE_MINUTES_ANS,
                     DATE_MONTH_ANS, DATE_YEAR_ANS, FAILURE_ANS,
                     INPUT_FAILURE_ANS, MEASURE_INPUT_ANS)
from database.crud import create_measure, create_user
from database.models import Measure, User
from handlers.date import normalize_date
from markups import date_markup, start_markup
from regexes import EMAIL_REGEX, MEASURE_REGEX

router = Router()


class NewMeasure(StatesGroup):
    measure = State()
    date = State()
    hour = State()
    minutes = State()
    day = State()
    month = State()
    year = State()


@router.message(StateFilter(None), Command('new'))
async def retrieve_mesurement(message: Message, state: FSMContext):
    if not message.from_user:
        await message.reply(FAILURE_ANS)
        return

    user = User(tg_id=message.from_user.id)

    create_user(user)

    await message.reply(
        MEASURE_INPUT_ANS
    )
    await state.set_state(NewMeasure.measure)


@router.message(
    NewMeasure.measure,
    F.text.regexp(MEASURE_REGEX)
)
async def retrieve_measure(message: Message, state: FSMContext):

    await state.update_data(measure=message.text)

    await message.answer(
        DATE_CHOICE_ANS,
        reply_markup=date_markup()
    )
    await state.set_state(NewMeasure.date)


@router.message(
    NewMeasure.measure
)
async def retrieve_measure_failure(message: Message, state: FSMContext):
    await message.answer(
        DATE_FAILURE_ANS
    )


'''Custom date.'''


@router.message(NewMeasure.date, F.text == 'Вручную')
async def trigger_custom_date(message: Message, state: FSMContext):
    await state.set_state(NewMeasure.hour)
    await message.answer(DATE_HOUR_ANS)


@router.message(NewMeasure.hour)
async def retrieve_hour(message: Message, state: FSMContext):
    text = message.text
    if not text or len(text) != 2 or not text.isdigit():
        await message.reply(INPUT_FAILURE_ANS)
        return

    await state.update_data(hour=int(text))

    await state.set_state(NewMeasure.minutes)
    await message.answer(DATE_MINUTES_ANS)


@router.message(NewMeasure.minutes)
async def retrieve_minutes(message: Message, state: FSMContext):
    text = message.text
    if not text or len(text) != 2 or not text.isdigit():
        await message.reply(INPUT_FAILURE_ANS)
        return

    await state.update_data(minutes=int(text))

    await state.set_state(NewMeasure.day)
    await message.answer(DATE_DAY_ANS)


@router.message(NewMeasure.day)
async def retrieve_day(message: Message, state: FSMContext):
    text = message.text
    if not text or len(text) != 2 or not text.isdigit():
        await message.reply(INPUT_FAILURE_ANS)
        return

    await state.update_data(day=int(text))

    await state.set_state(NewMeasure.month)
    await message.answer(DATE_MONTH_ANS)


@router.message(NewMeasure.month)
async def retrieve_month(message: Message, state: FSMContext):
    text = message.text
    if not text or len(text) != 2 or not text.isdigit():
        await message.reply(INPUT_FAILURE_ANS)
        return

    await state.update_data(month=int(text))

    await state.set_state(NewMeasure.year)
    await message.answer(DATE_YEAR_ANS)


@router.message(NewMeasure.year)
async def retrieve_year(message: Message, state: FSMContext):
    text = message.text
    if not text or len(text) != 4 or not text.isdigit():
        await message.reply(INPUT_FAILURE_ANS)
        return

    await state.update_data(year=int(text))

    data = await state.get_data()
    date = datetime(
        year=data['year'],
        month=data['month'],
        day=data['day'],
        hour=data['hour'],
        minute=data['minutes']
    )

    await state.update_data(date=date)
    data = await state.get_data()

    await state.clear()

    if not message.from_user:
        await message.reply(INPUT_FAILURE_ANS)
        return

    measure = Measure(**data, user_id=message.from_user.id)
    create_measure(measure)

    await message.reply(
        CONGRATS_ANS,
        reply_markup=start_markup()
    )


'''Date.'''


@router.message(NewMeasure.date, F.text == 'Сейчас')
async def retrieve_date_now(message: Message, state: FSMContext):
    await state.update_data(date=datetime.now())
    data = await state.get_data()
    await state.clear()

    if not message.from_user:
        await message.reply(FAILURE_ANS)
        return

    measure = Measure(**data, user_id=message.from_user.id)
    create_measure(measure)

    await message.reply(
        CONGRATS_ANS,
        reply_markup=start_markup()
    )


@router.message(
    NewMeasure.date, F.text.regexp(EMAIL_REGEX)
)
async def retrieve_date_custom(message: Message, state: FSMContext):
    await state.update_data(date=normalize_date(message.text or ''))
    data = await state.get_data()
    await state.clear()

    if not message.from_user:
        await message.reply(FAILURE_ANS)
        return

    measure = Measure(**data, user_id=message.from_user.id)
    create_measure(measure)

    await message.reply(
        CONGRATS_ANS,
        reply_markup=start_markup()
    )


@router.message(NewMeasure.date)
async def retrieve_date_failure(message: Message, state: FSMContext):
    await message.answer(
        DATE_FAILURE_ANS,
        reply_markup=date_markup()
    )
