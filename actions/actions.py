import time

from telebot import types
from config import TARGET_CHANNEL_ID, ADMIN_CHAT_ID, BOT_USERNAME
from string import Template
from config import POST_SAMPLE
from datetime import datetime


post_template = Template(POST_SAMPLE)

messages = {}

def send_approved_message(bot, message, author_chat_id, message_id_in_author_chat):
    print(f"DEBUG: {message}")
    if message.text:
        bot.send_message(TARGET_CHANNEL_ID, message.text)
    elif message.photo:
        bot.send_photo(TARGET_CHANNEL_ID, message.photo[-1].file_id, caption=message.caption)
    elif message.video:
        bot.send_video(TARGET_CHANNEL_ID, message.video.file_id, caption=message.caption)

    bot.send_message(author_chat_id, "🔥🔥Ваш пост был одобрен и отправлен в канал! ", reply_to_message_id= message_id_in_author_chat)
    bot.send_message(message.chat.id, "Отправлено в канал", reply_to_message_id= message.id)

def send_declined_message(bot, message, author_chat_id, message_id_in_author_chat):
    if message:
        bot.send_message(author_chat_id, "❌Ваш пост был отклонён.", reply_to_message_id=message_id_in_author_chat)

    bot.send_message(message.chat.id, "Отклонено", reply_to_message_id= message.id)

def send_delayed_message(bot, message, author_chat_id, message_id_in_author_chat):
    print("SENDDELAYEDMESSAGE func: ", message)
    bot.send_message(ADMIN_CHAT_ID, "Введите время отправки в формате дд.мм.гггг чч:мм:")
    target_message = message
    bot.register_next_step_handler(message, set_time, bot, author_chat_id, message_id_in_author_chat, target_message)

def set_time(message, bot, author_chat_id, message_id_in_author_chat, target_message):
    send_time = datetime.strptime(message.text, '%d.%m.%Y %H:%M')
    messages[message.id] = {'type': target_message.content_type, 'message': target_message, 'time': send_time}
    bot.send_message(ADMIN_CHAT_ID, f"Сообщение будет отправлено в {send_time}", reply_to_message_id=target_message.id)


def approved_from_user_message(bot, message, message_id_in_author_chat):
    confirmation_markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("✅Подтвердить", callback_data=f"admin_post_approve:{message.chat.id}:{message_id_in_author_chat}")
    decline_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"admin_post_decline:{message.chat.id}:{message_id_in_author_chat}")
    delay_button = types.InlineKeyboardButton("⏰Отложить", callback_data=f"admin_post_delay:{message.chat.id}:{message_id_in_author_chat}")
    confirmation_markup.add(approve_button, decline_button)
    confirmation_markup.add(delay_button)

    if message.text:
        text = f"{message.text}\n\n" + post_template.substitute(post_author=message.chat.username,
                                                                bot_username=BOT_USERNAME)
        bot.send_message(ADMIN_CHAT_ID, text, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Text message {message.text} from {message.chat.username} sent to admin-panel")
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author=message.chat.username, bot_username=BOT_USERNAME)
        bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Photo-message with caption {message.caption} from {message.chat.username} ")
    elif message.video:
        video_file_id = message.video.file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author=message.chat.username,
                                                                      bot_username=BOT_USERNAME)
        bot.send_video(ADMIN_CHAT_ID, video_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Video-message with caption {message.caption} from {message.chat.username} ")


def anonymous_from_user_message(bot, message, message_id_in_author_chat):
    confirmation_markup = types.InlineKeyboardMarkup()
    approve_button = types.InlineKeyboardButton("✅Подтвердить", callback_data=f"admin_post_approve:{message.chat.id}:{message_id_in_author_chat}")
    decline_button = types.InlineKeyboardButton("❌Отклонить", callback_data=f"admin_post_decline:{message.chat.id}:{message_id_in_author_chat}")
    confirmation_markup.add(approve_button, decline_button)

    if message.text:
        text = f"{message.text}\n\n" + post_template.substitute(post_author="Аноним",
                                                                bot_username=BOT_USERNAME)
        bot.send_message(ADMIN_CHAT_ID, text, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Text message {message.text} from {message.from_user.username} sent to admin-panel")
    elif message.photo:
        photo_file_id = message.photo[-1].file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author="Аноним",
                                                                      bot_username=BOT_USERNAME)
        bot.send_photo(ADMIN_CHAT_ID, photo_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")
        print(f"Photo-message with caption {message.caption} ")
    elif message.video:
        video_file_id = message.video.file_id
        message.caption = message.caption if message.caption else ''
        caption = f"{message.caption}\n\n" + post_template.substitute(post_author="Аноним",
                                                                      bot_username=BOT_USERNAME)
        bot.send_video(ADMIN_CHAT_ID, video_file_id, caption=caption, reply_markup=confirmation_markup)
        bot.send_message(message.chat.id, "Ваш пост успешно отправлен на рассмотрение!👍")


def declined_from_user_message(bot, author_chat_id):
    bot.send_message(author_chat_id, "Сообщение отменено. Жду новый вариант!")

def poll_delayed_messages(bot):
    current_time = datetime.now()
    for chat_id, data in messages.items():
        if data['time'] is not None and data['time'] <= current_time:
            match data['type']:
                case 'text':
                    bot.send_message(TARGET_CHANNEL_ID, data['message'].text)
                case 'photo':
                    bot.send_photo(TARGET_CHANNEL_ID, data['message'].photo[-1].file_id, caption=data['message'].caption)
                case 'video':
                    bot.send_video(TARGET_CHANNEL_ID, data['message'].video.file_id, caption=data['message'].caption)
            messages.pop(chat_id)
            break
