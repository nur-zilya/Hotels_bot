from telebot.handler_backends import State, StatesGroup


class UserInputInfo(StatesGroup):
    input_city = State()
    user_select_id = State()
    date_of_entry = State()
    departure_date = State()