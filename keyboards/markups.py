from aiogram.utils.keyboard import ReplyKeyboardBuilder


def date_markup():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Сейчас')
    return kb.as_markup()


def start_markup():
    kb = ReplyKeyboardBuilder()
    kb.button(text='/new')
    return kb.as_markup()
