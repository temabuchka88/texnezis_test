from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types


def function_keyborad():
    kb = ReplyKeyboardBuilder()
    kb.row(
        types.KeyboardButton(text="Обновить данные для парсинга"),
        types.KeyboardButton(text="Средняя цена товара"),
    )
    return kb.as_markup(resize_keyboard=True)