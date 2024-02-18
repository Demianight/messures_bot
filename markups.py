from aiogram.utils.keyboard import ReplyKeyboardBuilder


def date_markup():
    kb = ReplyKeyboardBuilder()
    kb.button(text='Сейчас')
    kb.button(text='Вручную')

    return kb.as_markup()


def start_markup():
    kb = ReplyKeyboardBuilder()
    kb.button(text='/start')
    kb.button(text='/new')
    kb.button(text='/show')
    kb.button(text='/show_raw')
    kb.button(text='/help')

    return kb.as_markup()
