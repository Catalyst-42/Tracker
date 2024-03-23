from time import time
from datetime import datetime, timedelta
from os import system, makedirs, path, name as os_name

from setup import setup

from utils import s, m, h, d, w
from utils import cyan, magenta, green, red, white
from utils import generate_activites_times

saved = True
timestamp = time()
activities = []

open("save.py", "a")  # Touch save file
from save import *

ARGS, ACTIVITIES = setup("tracker")
weeks = (timestamp - activities[0][1]) // (7*24*h) if activities else 0

def data_save(saved=True):
    if len(activities) == 0: return

    file = open("save.py", "w", encoding="utf-8")
    
    file.write(f"{saved = }\n{timestamp = }\nactivities = [ \n")
    for i in activities: file.write(f"\t{i},\n")
    file.write("]\n")

    file.close()

    # Weekly dump
    global weeks
    if saved and (timestamp - activities[0][1]) // (7*24*h) > weeks:
        weeks += 1

        filename = f"./dumps/week-{round(weeks)} ({activities[-1][2][:10]}).py"
        makedirs(path.dirname(filename), exist_ok=True)

        file = open(filename, "w", encoding="utf-8")

        file.write(f"{saved = }\ntimestamp = {activities[0][1] + weeks * 7*24*h}\nactivities = [ \n")
        for i in activities: file.write(f"\t{i},\n")
        file.write("]\n")

        file.close()

def stages_formatter(stages, verb=0):
    if verb:
        form = ["этапа", "этапов", "этапов"]
    else:
        form = ["этап", "этапа", "этапов"]
        
    last_digit = int(str(stages)[-1])
    last_2_digits = int(str(stages)[-2:])

    if last_digit == 1 and last_2_digits != 11: 
        return f"{magenta}{stages}{white} {form[0]}"
    
    if 1 <= last_digit <= 4 and (last_2_digits < 10 or last_2_digits > 20):
        return f"{magenta}{stages}{white} {form[1]}"
    
    return f"{magenta}{stages}{white} {form[2]}"

def analytics():
    if len(activities) == 0: return

    sum_all = timestamp - activities[0][1]
    print(
        f"Итоги {stages_formatter(len(activities), 1)} "
        f"({cyan}{timedelta(0, round(sum_all))}{white})"
    )

    activities_times = generate_activites_times(activities, timestamp)
    save_activities = set([i[0] for i in activities])

    # Analyze all data
    for activity_name in ACTIVITIES:
        if activity_name not in save_activities: continue
        
        activity_time = sum(activities_times[activity_name])
        if activity_time == 0: continue

        activity_percentage = activity_time/sum_all * 100
        activity_counter = len(activities_times[activity_name])
        activity_mean = activity_time / activity_counter

        print(
            f"{activity_name} ({stages_formatter(activity_counter)}) ({round(activity_percentage, 2)}%)\n"
            f"Всего: {cyan}{timedelta(0, round(activity_time))}{white}\n"
            f"В среднем {cyan}{timedelta(0, round(activity_mean))}{white} за этап\n"
        )

# Error cheking
if not saved:
    input(f"Последняя сессия была прервана: {activities[-1][0]} ({activities[-1][2]})")
    input(f"Добавление потерянного времени: {cyan}+{timedelta(0, int(time() - timestamp))}{white}\n")
    
    timestamp = time()
    data_save()

while True:
    system("cls" if os_name == "nt" else "clear")

    # Header
    activity = len(activities)
    stageline = "Последния сессия будет отображаться тут\n"
    
    if len(activities): 
        stageline = (
            f"Этап {magenta}{activity}{white}, {activities[-1][0]} "
            f"({datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')}) "
            f"({cyan}{timedelta(0, round(timestamp - activities[-1][1]))}{white})\n"
        )

    print(stageline)

    # Activities
    print("Выбор занятия:")
    for i, name in enumerate(ACTIVITIES):
        print(f"{green}{i+1}{white}: {name}")
    
    print()

    for i, name in enumerate([
        "Завершить сессию", 
        "Удалить последнее занятие", 
        "Изменить время последнего занятия", 
        "Добавить подпись к последнему занятию"
    ]):
        print(f"{green}{'edci'[i]}{white}: {name}")
    
    # Gain input
    session_id = input("\nВвод: ")
    if session_id.isdigit(): session_id = int(session_id)
    elif session_id in ('e', 'd', 'c', 'i'): session_id = len(ACTIVITIES) + "edci".index(session_id) + 1
    else: session_id = 0
        
    print()

    # Create new session
    if 1 <= session_id <= len(ACTIVITIES):
        activity_name = list(ACTIVITIES.keys())[session_id-1]

        # If activity repeat
        if len(activities) and activity_name == activities[-1][0]:
            print(f"Продолжение предыдущей сессии -> {activities[-1][0]} ({activities[-1][2]})")
            note = activities[-1][3]

        else:
            note = ''
            if activity_name == ARGS["ANOTHER"]:
                note = input("Подпись: ") or (ARGS["ANOTHER_DEFAULT_NOTE"])

            activities.append([
                f"{activity_name}", 
                timestamp,
                f"{datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')}",
                note
            ])
        
        # Wait for input to end session
        data_save(saved=False)
        input(f"<< {activity_name}{'' if not note else ' (' + note + ')'} >>")
        
        timestamp = time()
    
    # End sesstion
    if session_id == len(ACTIVITIES) + 1:
        data_save()
        analytics()
        exit()

    # Delete last activity
    if session_id == len(ACTIVITIES) + 2 and len(activities):
        print(f"Удалить: {activities[-1][0]} ({activities[-1][2]})?")
        if input("y/n: ").lower() == "y":
            activities.pop()
        else:
            input(f"\n{red}Удаление отменено{white}")

    # Change last activity time
    if session_id == len(ACTIVITIES) + 3:
        activity_name = activities[-1][0]
        activity_start_time = activities[-1][2]

        activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))
        print(f"Последний этап: {activity_name} ({activity_start_time}) {cyan}{activity_lasts}{white}")
        
        try: 
            allocated_time = eval(input("Этап закончился раньше на: "))
            
            if allocated_time < activity_lasts.total_seconds():
                timestamp -= allocated_time

                activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))
                input(f"\nНовая продолжительность этапа: {cyan}{activity_lasts}{white}")

            else:
                input(f"\n{red}Этап становится отрицательным, действие отменено{white}")
        
        except:
            input(f"\n{red}Действие отменено{white}")

    # Add a note
    if session_id == len(ACTIVITIES) + 4:
        activity_name = activities[-1][0]
        activity_start_time = activities[-1][2]
        activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))

        print(f"Добавление подписи к предыдущему занятию\n{activity_name} ({activity_start_time}) {cyan}{activity_lasts}{white}")
        note = input("\nПодпись: ")

        activities[-1][-1] = note

    data_save()
