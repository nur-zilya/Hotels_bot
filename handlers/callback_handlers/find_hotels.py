from loader import bot
from telebot.types import CallbackQuery
from states.user_states import UserInputState


@bot.callback_query_handlers(func=lambda call: call.data.isdigit())
def destination_id_callback(call: CallbackQuery) -> None:
    if call.data:
        bot.set_state(call.message.chat.id, UserInputState.destinationId)
        with bot.retrive_data(call.message.chat.id) as data:
            data['destination_id'] = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.set_state(call.message.chat.id, UserInputState.quantity_hotels)
        bot.send_message(call.message.chat.id, 'Сколько отелей вывести (не более 25)? ')
