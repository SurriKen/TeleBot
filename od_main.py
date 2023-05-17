import time

import telebot
from telebot import types

from yolo8 import YOLOv8

bot = telebot.TeleBot('6134635572:AAGkqaUA2vCVchHYgX1N22aoklRAwMRxVaA')
model = YOLOv8()


@bot.message_handler(commands=['start'])
def start(message):
    markups = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton("Detect objects on image")
    markups.row(btn1)
    btn4 = types.InlineKeyboardButton("Progress bar", callback_data='progress')
    markups.row(btn4)

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Hi! What do you want to do?",
        reply_markup=markups
    )
    # bot.register_next_step_handler(
    #     message=message,
    #     callback=on_click
    # )

@bot.message_handler()
def main(message):
    if message.text == 'Detect objects on image':
        # print(message)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Please load an image for Object Detection",
        )
        bot.register_next_step_handler(
            message=message,
            callback=yolo_detect_image
        )
    elif message.text == 'Progress bar':
        msg = bot.send_message(
            text=f'Progressing 0 %...',
            chat_id=message.chat.id,
        )
        print(msg)
        for i in range(100):
            # bot.delete_message(
            #     chat_id=message.chat.id,
            #     message_id=message.message_id - 1,
            # )
            bot.edit_message_text(
                text=f'Progressing {i} %...',
                chat_id=msg.chat.id,
                message_id=msg.message_id,
            )
            time.sleep(1)
        bot.send_message(
            text=f'Progress is finished',
            chat_id=message.chat.id,
            # message_id=message.message_id,
        )


def yolo_detect_image(message):
    if not message.photo:
        bot.send_message(
            chat_id=message.chat.id,
            text=f"message doesn't contain image, please check that file has image extention like '.png', '.jpg', etc",
        )
    else:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        dowloaded_file = bot.download_file(file_info.file_path)

        with open('temp/image.jpg', 'wb') as new_file:
            new_file.write(dowloaded_file)

        model.detect_image('temp/image.jpg')

        file = open('temp/predict.jpg', 'rb')
        bot.send_photo(
            chat_id=message.chat.id,
            photo=file
        )
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'Progress bar':
        for i in range(100):
            bot.edit_message_text(
                text=f'Progressing {i} %...',
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
            )
            time.sleep(1)
        bot.edit_message_text(
            text=f'Progress is finished',
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
        )

bot.polling(none_stop=True)