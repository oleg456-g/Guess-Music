import telebot
import os
from config import TOKEN  # Токен бота в Telegram
from random import randint

# Инициализируем бота
bot = telebot.TeleBot(TOKEN)
# Создаём словарь, где ключ - название песни, значение - путь к песни
audios = dict()
# Получаем песни из папки
path_to_files = os.getenv('USERPROFILE')+'\\Desktop\\'
for file in os.listdir(path_to_files):
    if file.endswith('.mp3'):
        audios.update({file[:-4].replace('-', ' '): os.path.join(path_to_files, file)})


# Создаём inline кнопки
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button1 = telebot.types.KeyboardButton('Начать игру.')
keyboard.add(button1)


# Проверяем ответ пользователя
def check_answer(message, audio):
    global audios
    correct_answer = audio[0]
    if message.text.lower() == correct_answer.lower():
        bot.send_message(message.chat.id, 'Правильно, молодец!')
        # Удаляем песню из словаря при правильном ответе
        audios.pop(audio[0], audio[1])
    else:
        bot.send_message(message.chat.id, 'Неправильно!')


# Создаём функцию в ответ на команду start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет, я развлекательный бот. Попробуй угадать музыку.', reply_markup=keyboard)


# Создаём функцию игры
@bot.message_handler(content_types=['text'])
def play(message):
    if message.text == 'Начать игру.':
        # Путь к аудио трекам
        audios_path = list(audios.items())
        audio = audios_path[randint(0, len(audios_path))-1]
        # Отправляем аудио
        with open(audio[1], 'rb') as audio_path:
            msg = bot.send_audio(message.chat.id, audio_path)
            bot.register_next_step_handler(msg, check_answer, audio)


bot.infinity_polling()
