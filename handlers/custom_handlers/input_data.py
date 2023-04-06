from loader import bot
from telebot.types import Message
import datetime
from states.user_states import UserInputState
import keyboards.inline
from keyboards.calendar import Calendar
import utils


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def low_high_best_handler(message: Message) -> None:
    bot.set_state(message.chat.id, UserInputState.command)
    with bot.retrive_data(message.chat.id) as data:
        data.clear()
        data['command'] = message.text
        data['sort'] = check_command(message.text)
        data['date_time'] = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        data['chat_id'] = message.chat.id
    bot.set_state(message.chat.id, UserInputState.input_city)
    bot.send_message(message.from_user.id, "Введите город, в котором нужно найти отель (на латинице): ")


@bot.message_handler(state=UserInputState.input_city)
def input_city(message: Message) -> None:
    with bot.retrieve_data(message.chat.id) as data:
        data['input_city'] = message.text
        url = "https://hotels4.p.rapidapi.com/locations/v3/search"
        querystring = {"q": message.text, "locale": "en_US"}
        response_cities = utils.api_request.request('GET', url, querystring)
        if response_cities.status_code == 200:
            possible_cities = utils.processing_json.get_city(response_cities.text)
            keyboards.inline.create_buttons.show_cities_buttons(message, possible_cities)
        else:
            bot.send_message(message.chat.id, f"Что-то пошло не так, код ошибки: {response_cities.status_code}")
            bot.send_message(message.chat.id, "Нажмите кнопку еще раз и введите город. ")
            data.clear()


@bot.message_handler(state=UserInputState.quantity_hotels)
def input_quantity(message: Message) -> None:
    if message.text.isdigit():
        if 0 < int(message.text) <= 25:
            with bot.retrieve_data(message.chat.id) as data:
                data['inquiry_hotels'] = message.text
            bot.set_state(message.chat.id, UserInputState.priceMin)
            bot.set_state(message.chat.id, 'Введите минимальную стоимость отеля в USD')
        else:
            bot.send_message(message.chat.id, 'Ошибка! Число должно быть от 1 до 25 ')

    else:
        bot.send_message(message.chat.id, "Ошибка! Вы ввели не число!")


@bot.message_handler(state=UserInputState.priceMin)
def input_price_min(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['price_min'] = message.text
        bot.set_state(message.chat.id, UserInputState.priceMax)
        bot.set_message(message.chat.id, 'Введите максимальную стоимость отеля в USD')
    else:
        bot.send_message(message.chat.id, "Ошибка! Вы ввели не число!")


@bot.message_handler(state=UserInputState.priceMax)
def input_price_max(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            if int(data['price_min']) < int(message.text):
                data['price_max'] = message.text
                keyboards.inline.create_buttons.show_buttons_photo_need_yes_no(message)
            else:
                bot.send_message(message.chat.id, 'Максимальная цена должна быть больше минимальной. Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.photo_count)
def input_photo_quantity(message: Message) -> None:
    if message.text.isdigit():
        if 0 < int(message.text) <= 10:
            with bot.retrieve_data(message.chat.id) as data:
                data['photo_count'] = message.text
            my_calendar(message, 'заезда')
        else:
            bot.send_message(message.chat.id, 'Число фотографий должно быть в диапазоне от 1 до 10! Повторите ввод!')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.landmarkIn)
def input_landmark_in(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_in'] = message.text
        bot.set_state(message.chat.id, UserInputState.landmarkOut)
        bot.send_message(message.chat.id, 'Введите конец диапазона расстояния от центра (в милях).')
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


@bot.message_handler(state=UserInputState.landmarkOut)
def input_landmark_out(message: Message) -> None:
    if message.text.isdigit():
        with bot.retrieve_data(message.chat.id) as data:
            data['landmark_out'] = message.text
            utils.show_data_and_find_hotels.print_data(message, data)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Вы ввели не число! Повторите ввод!')


def check_command(command: str) -> str:
    if command == '/bestdeal':
        return 'DISTANCE'
    elif command == '/lowprice' or command == '/highprice':
        return 'PRICE_LOW_TO_HIGH'


bot_calendar = Calendar()


def my_calendar(message: Message, word: str) -> None:
    bot.send_message(message.chat.id, f"Выберите дату {word}", reply_markup=bot_calendar.create_calendar())


