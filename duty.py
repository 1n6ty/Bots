import datetime
import json
from threading import Timer

def start_inf_duty_msg(bot, chat_id, message_thread_id, duty_d, duty_table_path):
    cur_datetime = datetime.datetime.now()

    duty_pmi = any([(datetime.datetime.strptime(i[0], "%d.%m.%y") < cur_datetime < datetime.datetime.strptime(i[1], "%d.%m.%y")) for i in duty_d["pmi_duty"]])
    duty_fpmi = any([(datetime.datetime.strptime(i[0], "%d.%m.%y") < cur_datetime < datetime.datetime.strptime(i[1], "%d.%m.%y")) for i in duty_d["fpmi_duty"]])

    names = "\n".join(['| ' + i for i in duty_d["group_list"][int(duty_d["last_duty_id"]): int(duty_d["last_duty_id"]) + 2]])
    bot.send_message(chat_id=chat_id, message_thread_id=message_thread_id, text=f'Дежурные на сегодня:\n\n{names}\n\nДежурные ПМИ: {"Да" if duty_pmi else "Нет"}\nДежурные потока: {"Да" if duty_fpmi else "Нет"}')

    duty_d["last_duty_id"] += 2
    if duty_d["last_duty_id"] >= len(duty_d["group_list"]):
        duty_d["last_duty_id"] = 0

    with open(duty_table_path, 'w', encoding='utf-8') as duty:
        duty.write(json.dumps(duty_d))

    delta = datetime.timedelta(days=1) if cur_datetime.weekday() != 5 else datetime.timedelta(days=2)

    nex_time = (cur_datetime + delta).replace(hour=7, minute=0, second=0, microsecond=0)
    t = Timer((nex_time - cur_datetime).total_seconds(), start_inf_duty_msg, args=[bot, chat_id, message_thread_id, duty_d, duty_table_path])
    t.start()