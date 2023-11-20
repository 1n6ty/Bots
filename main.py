import telebot

import datetime
from threading import Timer
from pathlib import Path
import json

BASE_DIR = Path(__file__).parent

with open(BASE_DIR / 'table.json', 'r') as f:
    table = json.loads(f.read())

with open(BASE_DIR / 'secret.json', 'r') as f:
    secret = json.loads(f.read())
    token = secret['bot_token']
    chat_id = secret['chat_id']

bot = telebot.TeleBot(token)

def add2table(text: str, current_ind: int):
    global table

    if current_ind == 0:
        time_d = datetime.timedelta(days=1)
    elif current_ind == 1:
        time_d = datetime.timedelta(days=3)
    elif current_ind == 2:
        time_d = datetime.timedelta(days=6)
    elif current_ind == 3:
        time_d = datetime.timedelta(days=14)
    elif current_ind == 4:
        time_d = datetime.timedelta(days=30)
    elif current_ind == 5:
        time_d = datetime.timedelta(days=60)
    else:
        return
    
    day_rep = (datetime.datetime.now().date() + time_d).strftime("%m/%d/%y")

    if day_rep in table:
        table[day_rep].append([text, current_ind + 1])
    else:
        table[day_rep] = [[text, current_ind + 1]]
    
def send_note(bot, chat_id):
    day_rep = datetime.datetime.now().date()

    if day_rep.strftime("%m/%d/%y") in table:
        bot.send_message(chat_id, f'{day_rep.strftime("%m/%d/%y")}\n' + "\n".join([i[0] for i in table[day_rep.strftime("%m/%d/%y")]]))
    else:
        bot.send_message(chat_id, 'Ничего на сегодня нет')
    
    miss_dates = [i for i in table if datetime.datetime.strptime(i, '%m/%d/%y').date() < day_rep]
    
    for d in miss_dates:
        for i in table[d]:
            add2table(*i)

    for d in miss_dates:
        del table[d]
    
    cur_datetime = datetime.datetime.now()
    delta = datetime.timedelta(days=1)
    nex_time = (cur_datetime + delta).replace(hour=17, minute=0, second=0, microsecond=0)
    
    t = Timer((nex_time - cur_datetime).total_seconds(), send_note, args=[bot, chat_id])
    t.start()

@bot.message_handler(commands=['start'])
def start_message(msg):
    bot.send_message(msg.chat.id, f'Chat id - {msg.chat.id}')
    
    send_note(bot, chat_id)

@bot.message_handler(content_types='text')
def message_reply(msg):
    if not (str(msg.chat.id) == chat_id):
        return

    add2table(msg.text, 0)
    
    with open(BASE_DIR / 'table.json', 'w') as f:
        f.write(json.dumps(table))

bot.infinity_polling(timeout=10, long_polling_timeout = 5)