import os

import ffmpeg
import moviepy.editor as mp

import telebot
from telebot import types

from utils import load_video_from_google_drive, load_video_from_yandex_disc, load_video_from_youtube
from yolo8 import YOLOv8

bot = telebot.TeleBot('6134635572:AAGkqaUA2vCVchHYgX1N22aoklRAwMRxVaA')
google_api = 'AIzaSyCUto8qWyQQluo-PN4PlhVzh_IidC8PHDY'
source_url = None
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
    btn3 = types.KeyboardButton("Detect objects on video (through link)")
    markups.row(btn3)
    send_text_message(message, f"Hi! What do you want to do?", markups)


@bot.message_handler()
def main(message):
    print(message)
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
    elif message.text == 'Detect objects on video (through link)':
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("GoogleDisk", callback_data='google_disk')
        btn2 = types.InlineKeyboardButton("YandexDisk", callback_data='yandex_disk')
        btn3 = types.InlineKeyboardButton("Youtube", callback_data='youtube')
        markup.row(btn1, btn2, btn3)
        bot.reply_to(
            message=message,
            text=f"Please choose video source for loading",
            reply_markup=markup
        )
        bot.register_next_step_handler(
            message=message,
            callback=yolo_detect_image
        )


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global source_url
    if callback.data == 'google_disk':
        source_url = 'google_disk'
        pass
    elif callback.data == 'yandex_disk':
        source_url = 'yandex_disk'
        pass
    elif callback.data == 'youtube':
        source_url = 'youtube'
        bot.send_message(
            text='Please send link on youtube video',
            chat_id=callback.message.chat.id,
        )
        bot.register_next_step_handler(
            message=callback.message,
            callback=yolo_detect_video_from_link
        )
        pass


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


def video_detection(message):
    clip = mp.VideoFileClip("temp/video.mp4")
    process_time = clip.fps * clip.duration * 0.04
    if round(process_time % 60, -1) == 60:
        process_time = f" (about {int(process_time // 60 + 1)} min 00 sec)"
    elif process_time // 60 > 0:
        process_time = f" (about {int(process_time // 60)} min {int(round(process_time % 60, -1))} sec)"
    else:
        process_time = f" (about {int(round(process_time % 60, -1))} sec)"
    send_text_message(message, f"Video detection is in process. It takes a bit of time{process_time}")
    try:
        model.detect_video('temp/video.mp4')
        send_text_message(message, model.message)
    except:
        send_text_message(message, 'There is a problem with AI, please try another video')

    clip = mp.VideoFileClip("temp/predict.mp4")
    # make the height 360px ( According to moviePy documenation The width is then computed so that the width/height ratio is conserved.)
    if clip.size[1] > 360:
        clip_resized = clip.resize(360 / clip.size[1])
        os.remove('temp/predict.mp4')
        clip_resized.write_videofile("temp/predict.mp4")

    file = open('temp/predict.mp4', 'rb')
    vid = ffmpeg.probe("temp/predict.mp4")
    vid_zize = int(vid['format']['size']) / 1024 / 1024
    print(f"Resulted video has a size {round(vid_zize, 1)} MB")
    if vid_zize > 50:
        send_text_message(
            message,
            f"Resulted video has size {round(vid_zize, 1)} MB which is more than 50 MB and can't be loaded in chat"
        )
        return
    try:
        bot.send_video(
            chat_id=message.chat.id,
            video=file,
            timeout=30
        )

    except Exception as err:
        send_text_message(message, err)
        return


def yolo_detect_video(message):
    if not message.video:
        send_text_message(message, "message doesn't contain video, please check that message contain a video file")
    else:
        fileID = message.video.file_id
        try:
            send_text_message(message, 'File is downloading on server...')
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

        video_detection(message)


def yolo_detect_video_from_link(message):
    link = message.text
    if link and source_url == 'google_disk':
        load_video_from_google_drive(google_drive_link=link, google_api=google_api)
    elif link and source_url == 'yandex_disk':
        load_video_from_yandex_disc(public_key=link)
    elif link and source_url == 'youtube':
        send_text_message(message, 'File is downloading on server...')
        st = load_video_from_youtube(link=link)
        if st[0]:
            send_text_message(message, 'Download is completed successfully')
        else:
            send_text_message(message, st[1])

    video_detection(message)


bot.polling(none_stop=True)
