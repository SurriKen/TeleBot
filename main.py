import telebot
import webbrowser
import sqlite3

from PIL import Image
from telebot import types

bot = telebot.TeleBot('6134635572:AAGkqaUA2vCVchHYgX1N22aoklRAwMRxVaA')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markups = types.InlineKeyboardMarkup()
    # markups.add(types.InlineKeyboardButton("Start", url='https://github.com/SurriKen/TeleBot'))
    # markups.add(types.InlineKeyboardButton("My github", url='https://github.com/SurriKen/TeleBot'))
    btn1 = types.InlineKeyboardButton("Google it", url='https://google.com')
    markups.row(btn1)
    btn2 = types.InlineKeyboardButton("Delete file", callback_data='delete')
    btn3 = types.InlineKeyboardButton("Edit text", callback_data='edit')
    markups.row(btn2, btn3)

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    dowloaded_file = bot.download_file(file_info.file_path)

    with open('temp/image.jpg', 'wb') as new_file:
        new_file.write(dowloaded_file)

    # img = Image.open(file.file_path)
    # img.save('temp/image.jpg')
    bot.reply_to(
        message=message,
        text='Nice Photo!',
        reply_markup=markups
    )


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id - 1,
        )
    elif callback.data == 'edit':
        bot.edit_message_text(
            text='Edit text',
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
        )


@bot.message_handler(commands=['start'])
def start(message):
    markups = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton("Show Image")
    markups.row(btn1)
    btn2 = types.KeyboardButton("Google it")
    btn3 = types.KeyboardButton("Github")
    markups.row(btn2, btn3)
    btn4 = types.InlineKeyboardButton("Progress bar", callback_data='progress')
    markups.row(btn4)

    bot.send_message(
        chat_id=message.chat.id,
        text=f"Hi, {message.from_user.first_name} {message.from_user.last_name}!",
        reply_markup=markups
    )
    # file = open('temp/maxresdefault.jpg', 'rb')
    # bot.send_photo(
    #     chat_id=message.chat.id,
    #     photo=file
    # )
    # while True:
    bot.register_next_step_handler(
        message=message,
        callback=on_click
    )


def on_click(message):
    if message.text == 'Google it':
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Google it for yourself",
        )
    elif message.text == 'Github':
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Github? Google it for itself!",
        )
    elif message.text == 'Show Image':
        file = open('temp/maxresdefault.jpg', 'rb')
        bot.send_photo(
            chat_id=message.chat.id,
            photo=file
        )


@bot.message_handler(commands=['start', 'main', 'test'])
def main(message):
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Hi, {message.from_user.first_name} {message.from_user.last_name}!"
    )


@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="<b>Help</b> <em><u>information</u></em>",
        parse_mode='html'
    )


@bot.message_handler(commands=['site'])
def site(message):
    webbrowser.open('https://github.com/SurriKen/TeleBot')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'hi':
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Hi, {message.from_user.first_name}"
        )
    elif message.text.lower() == 'id':
        bot.reply_to(
            message=message,
            text=f"User ID: {message.from_user.id}"
        )


bot.polling(none_stop=True)

m = {
    'content_type': 'text',
    'id': 24,
    'message_id': 24,
    'from_user': {
        'id': 394122946,
        'is_bot': False,
        'first_name': 'Denis',
        'username': 'Denis_Yurchuk',
        'last_name': 'Yurchuk',
        'language_code': 'en',
        'can_join_groups': None,
        'can_read_all_group_messages': None,
        'supports_inline_queries': None,
        'is_premium': None,
        'added_to_attachment_menu': None
    },
    'date': 1684268965,
    'chat': {
        'id': 394122946,
        'type': 'private',
        'title': None,
        'username': 'Denis_Yurchuk',
        'first_name': 'Denis',
        'last_name': 'Yurchuk',
        'is_forum': None,
        'photo': None,
        'bio': None,
        'join_to_send_messages': None,
        'join_by_request': None,
        'has_private_forwards': None,
        'has_restricted_voice_and_video_messages': None,
        'description': None,
        'invite_link': None,
        'pinned_message': None,
        'permissions': None,
        'slow_mode_delay': None,
        'message_auto_delete_time': None,
        'has_protected_content': None,
        'sticker_set_name': None,
        'can_set_sticker_set': None,
        'linked_chat_id': None,
        'location': None,
        'active_usernames': None,
        'emoji_status_custom_emoji_id': None,
        'has_hidden_members': None,
        'has_aggressive_anti_spam_enabled': None
    },
    'sender_chat': None,
    'forward_from': None,
    'forward_from_chat': None,
    'forward_from_message_id': None,
    'forward_signature': None,
    'forward_sender_name': None,
    'forward_date': None,
    'is_automatic_forward': None,
    'reply_to_message': None,
    'via_bot': None,
    'edit_date': None,
    'has_protected_content': None,
    'media_group_id': None,
    'author_signature': None,
    'text': '/start',
    'entities': ['<telebot.types.MessageEntity object at 0x101dd6a30>'],
    'caption_entities': None,
    'audio': None,
    'document': None,
    'photo': None,
    'sticker': None,
    'video': None,
    'video_note': None,
    'voice': None,
    'caption': None,
    'contact': None,
    'location': None,
    'venue': None,
    'animation': None,
    'dice': None,
    'new_chat_member': None,
    'new_chat_members': None,
    'left_chat_member': None,
    'new_chat_title': None,
    'new_chat_photo': None,
    'delete_chat_photo': None,
    'group_chat_created': None,
    'supergroup_chat_created': None,
    'channel_chat_created': None,
    'migrate_to_chat_id': None,
    'migrate_from_chat_id': None,
    'pinned_message': None,
    'invoice': None,
    'successful_payment': None,
    'connected_website': None,
    'reply_markup': None,
    'message_thread_id': None,
    'is_topic_message': None,
    'forum_topic_created': None,
    'forum_topic_closed': None,
    'forum_topic_reopened': None,
    'has_media_spoiler': None,
    'forum_topic_edited': None,
    'general_forum_topic_hidden': None,
    'general_forum_topic_unhidden': None,
    'write_access_allowed': None,
    'user_shared': None,
    'chat_shared': None,
    'json': {
        'message_id': 24,
        'from': {
            'id': 394122946,
            'is_bot': False,
            'first_name': 'Denis',
            'last_name': 'Yurchuk',
            'username': 'Denis_Yurchuk',
            'language_code': 'en'},
        'chat': {
            'id': 394122946,
            'first_name': 'Denis',
            'last_name': 'Yurchuk',
            'username': 'Denis_Yurchuk',
            'type': 'private'
        },
        'date': 1684268965,
        'text': '/start',
        'entities': [{'offset': 0, 'length': 6, 'type': 'bot_command'}]
    }
}
