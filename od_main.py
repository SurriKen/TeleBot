import os
import moviepy.editor as mp

import telebot
from telebot import types

from yolo8 import YOLOv8

bot = telebot.TeleBot('6134635572:AAGkqaUA2vCVchHYgX1N22aoklRAwMRxVaA')
model = YOLOv8()


def send_text_message(message, text, reply_markup=None):
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=reply_markup
    )

@bot.message_handler(commands=['start'])
def start(message):
    markups = types.ReplyKeyboardMarkup()

    btn1 = types.KeyboardButton("Detect objects on image")
    markups.row(btn1)
    btn2 = types.KeyboardButton("Detect objects on video")
    markups.row(btn2)
    send_text_message(message, f"Hi! What do you want to do?", markups)


@bot.message_handler()
def main(message):
    if message.text == 'Detect objects on image':
        send_text_message(message, f"Please load an image for Object Detection")

        bot.register_next_step_handler(
            message=message,
            callback=yolo_detect_image
        )

    elif message.text == 'Detect objects on video':
        send_text_message(message, f"Please load a video for Object Detection")
        bot.register_next_step_handler(
            message=message,
            callback=yolo_detect_video
        )


def yolo_detect_image(message):
    if not message.photo:
        send_text_message(message, "message doesn't contain image, please check that file has an image")
    else:
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        dowloaded_file = bot.download_file(file_info.file_path)

        if os.path.isfile('temp/image.jpg'):
            os.remove('temp/image.jpg')

        with open('temp/image.jpg', 'wb') as new_file:
            new_file.write(dowloaded_file)

        model.detect_image('temp/image.jpg')

        file = open('temp/predict.jpg', 'rb')
        send_text_message(message, model.message)
        if model.status:
            bot.send_photo(
                chat_id=message.chat.id,
                photo=file
            )


def yolo_detect_video(message):
    if not message.video:
        send_text_message(message, "message doesn't contain video, please check that message contain a video file")
    else:
        fileID = message.video.file_id
        try:
            send_text_message(message, 'File is loading on server...')
            file_info = bot.get_file(fileID)
            dowloaded_file = bot.download_file(file_info.file_path)
        except Exception as err:
            send_text_message(message, err)
            send_text_message(message, 'File is too big, please choose video less than 20 MB')
            return

        if os.path.isfile('temp/video.mp4'):
            os.remove('temp/video.mp4')

        with open('temp/video.mp4', 'wb') as new_file:
            new_file.write(dowloaded_file)

        send_text_message(message, "Video detection is in process. It takes a bit of time")
        try:
            model.detect_video('temp/video.mp4')
            send_text_message(message, model.message)
        except:
            send_text_message(message, 'There is a problem with AI, please try another video')

        clip = mp.VideoFileClip("temp/predict.mp4")
        # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
        clip_resized = clip.resize(0.6)
        os.remove('temp/predict.mp4')
        clip_resized.write_videofile("temp/predict.mp4")

        file = open('temp/predict.mp4', 'rb')
        try:
            bot.send_video(
                chat_id=message.chat.id,
                video=file,
                timeout=30
            )
        except Exception as err:
            send_text_message(message, err)
            bot.send_document(
                chat_id=message.chat.id,
                document=file,
                timeout=30
            )
            # send_text_message(message, 'Problem with loading in chat')


bot.polling(none_stop=True)
