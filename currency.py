import requests
import telebot
from currency_converter import CurrencyConverter

bot = telebot.TeleBot('6134635572:AAGkqaUA2vCVchHYgX1N22aoklRAwMRxVaA')
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    markups = telebot.types.ReplyKeyboardMarkup()
    btn1 = telebot.types.KeyboardButton("Convert")
    markups.row(btn1)
    bot.send_message(message.chat.id, 'Hi! Welcome to currency converter bot', reply_markup=markups)

@bot.message_handler()
def main(message):
    if message.text == 'Convert':
        bot.send_message(message.chat.id, 'Input the money amount')
        bot.register_next_step_handler(
            message=message,
            callback=summa
        )

def summa(message):
    global amount
    try:
        amount = float(message.text.strip().lower())
    except ValueError:
        bot.send_message(
            chat_id=message.chat.id,
            text="Incorrect number. Inpunt amount again"
        )
        bot.register_next_step_handler(message, summa)
        return

    if amount > 0:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        btn1 = telebot.types.InlineKeyboardButton("EUR/RUB", callback_data='eur/rub')
        btn2 = telebot.types.InlineKeyboardButton("RUB/EUR", callback_data='rub/EUR')
        btn3 = telebot.types.InlineKeyboardButton("USD/RUB", callback_data='usd/rub')
        btn4 = telebot.types.InlineKeyboardButton("RUB/USD", callback_data='rub/usd')
        btn5 = telebot.types.InlineKeyboardButton("CNY/RUB", callback_data='cny/rub')
        btn6 = telebot.types.InlineKeyboardButton("RUB/CNY", callback_data='rub/cny')
        btn7 = telebot.types.InlineKeyboardButton("EUR/USD", callback_data='eur/usd')
        btn8 = telebot.types.InlineKeyboardButton("USD/EUR", callback_data='USD/EUR')
        btn9 = telebot.types.InlineKeyboardButton("Other pair", callback_data='else')
        markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9)

        bot.send_message(
            chat_id=message.chat.id,
            text="Choose currensy pair",
            reply_markup=markup
        )
    else:
        bot.send_message(
            chat_id=message.chat.id,
            text="Amount must be more than 0. Inpunt amount again"
        )
        bot.register_next_step_handler(message, summa)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    val = call.data.upper().split('/')
    if val[1] == "RUB":
        res = currency.convert(
            amount=1,
            currency=val[1],
            new_currency=val[0]
        )
        res = amount / res
    else:
        res = currency.convert(
            amount=amount,
            currency=val[0],
            new_currency=val[1]
        )
    bot.send_message(
        chat_id=call.message.chat.id,
        text=f'Result: {round(res, 2)} {val[1].lower()}'
    )



bot.polling(none_stop=True)