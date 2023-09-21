import telebot

from pathlib import Path
import json

from attendance import start_inf_pooling_attendance
from duty import start_inf_duty_msg

BASE_DIR = Path(__file__).resolve().parent

with open(BASE_DIR / 'secret.json', 'r', encoding='utf-8') as secret:
    secret_d = json.loads(secret.read())

with open(BASE_DIR / 'duty_table.json', 'r', encoding='utf-8') as duty:
    duty_d = json.loads(duty.read())

bot = telebot.TeleBot(secret_d["bot_token"])

start_service = {
    "attendance": False,
    "duty": False
}

@bot.message_handler(commands=['start'])
def start_msg(msg):
    if (not start_service['attendance']) and int(msg.message_thread_id) == int(secret_d['attendance_thread_id']):
        start_inf_pooling_attendance(bot, msg.chat.id, msg.message_thread_id)
        start_service["attendance"] = True
    
    if (not start_service['duty']) and int(msg.message_thread_id) == int(secret_d['duty_thread_id']):
        start_inf_duty_msg(bot, msg.chat.id, msg.message_thread_id, duty_d, BASE_DIR / 'duty_table.json')
        start_service["duty"] = True

bot.infinity_polling(timeout = 10, long_polling_timeout = 5)