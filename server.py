import telebot
import sqlite3
from threading import Lock

TOKEN = '7162058057:AAGt5hweR-7_FCK1zhkLf-HaF6OE-oOLhzA'

bot = telebot.TeleBot(TOKEN)

conn = sqlite3.connect(r"F:\WP\DB.db", check_same_thread=False)
cursor = conn.cursor()

def create_table():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            message TEXT
        )
    ''')

create_table()
conn.commit()

# Блокировка для исправления ошибки при подключения к SQLite
db_lock = Lock()

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "---ИНСТРУКЦИЯ ПО ДОНОСУ---")

# /don
@bot.message_handler(commands=['don'])
def cum(message):

    bot.send_message(message.chat.id, "Донесите информацию строго по инструкции: ")

    bot.register_next_step_handler(message, save_message)

def save_message(message):
    user_id = message.from_user.id
    text = message.text

    with db_lock:

        cursor.execute('INSERT INTO messages (user_id, message) VALUES (?, ?)', (user_id, text))
        conn.commit()

    bot.send_message(message.chat.id, "Информация сохранена!")

bot.polling()