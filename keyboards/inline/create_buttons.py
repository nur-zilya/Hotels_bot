from loader import bot
from telebot import types
from loguru import logger
from telebot.types import Message, Dict


def show_buttons_photo(message: Message) -> None:
    keyboard_yes_no = types.InlineKeyboardMarkup()
    keyboard_yes_no.add(types.InlineKeyboardButton(text='да', callback_data='yes'))
    keyboard_yes_no.add(types.InlineKeyboardButton(text='нет', callback_data='no'))
    bot.send_message(message.chat.id, "Нужно вывести фото?", reply_markup=keyboard_yes_no)


def show_cities_buttons(message: Message, possible_cities: Dict) -> None:
    keyboard_cities = types.InlineKeyboardMarkup()
    for key, value in possible_cities.items():
        keyboard_cities.add(types.InlineKeyboardButton(text=value["regionNames"], callback_data=value["gaiaId"]))
    bot.send_message(message.from_user.id, "Пожалуйста, выберите город", reply_markup=keyboard_cities)