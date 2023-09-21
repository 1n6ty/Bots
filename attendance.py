from threading import Timer
import datetime

def start_inf_pooling_attendance(bot, chat_id, message_thread_id):
    cur_datetime = datetime.datetime.now()
    
    bot.send_poll(chat_id=chat_id, message_thread_id=message_thread_id, question=f'{cur_datetime.strftime("%d.%m")}', options=["Я на парах", "Я нет"], is_anonymous=False)

    delta = datetime.timedelta(days=1) if cur_datetime.weekday() != 5 else datetime.timedelta(days=2)
    
    nex_time = (cur_datetime + delta).replace(hour=7, minute=0, second=0, microsecond=0)
    t = Timer((nex_time - cur_datetime).total_seconds(), start_inf_pooling_attendance, args=[bot, chat_id, message_thread_id])
    t.start()