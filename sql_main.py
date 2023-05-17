import telebot
import webbrowser
import sqlite3

from telebot import types

bot = telebot.TeleBot('6134635572:AAGkqaUA2vCVchHYgX1N22aoklRAwMRxVaA')
name = ''

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect(
        database='test.sql'
    )
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users '
                '(id int auto_increment primary key, name varchar(50), password varchar(50)) ')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(
        chat_id=message.chat.id,
        text='Hi! Lets make a registration, input your name'
    )
    bot.register_next_step_handler(
        message=message,
        callback=user_name
    )


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(
        chat_id=message.chat.id,
        text='Input your password'
    )
    bot.register_next_step_handler(
        message=message,
        callback=user_password
    )


def user_password(message):
    password = message.text.strip()
    conn = sqlite3.connect(
        database='test.sql'
    )
    cur = conn.cursor()
    cur.execute('INSERT INTO users (name, password) VALUES ("%s", "%s")' % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("List of users", callback_data='users'))
    bot.send_message(
        chat_id=message.chat.id,
        text='User has been registered',
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect(
        database='test.sql'
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users:
        info += f"Name: {el[1]}, Pass: {el[2]}\n"
    cur.close()
    conn.close()

    bot.send_message(
        chat_id=call.message.chat.id,
        text=info
    )


bot.polling(none_stop=True)