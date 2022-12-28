import time
import os

from datetime import datetime, timedelta
from constants import *

timestamp = time.time()
saved = True
activities = []

open("save.py", "a")
from save import *

weeks = (timestamp - activities[0][1]) // (7*24*h) if activities else 0
def data_save(saved=True):
    global weeks
    file = open("save.py", "w")
    
    file.write(f"{saved = }\n{timestamp = }\nactivities = [ \n")
    for i in activities: file.write(f"\t{i},\n")
    file.write("]\n")

    file.close()

    # weekly dump
    if len(activities) and saved and (timestamp - activities[0][1]) // (7*24*h) > weeks:
        weeks += 1

        filename = f"./dumps/week-{round(weeks)} ({activities[-1][2][:10]}).py"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        file = open(filename, "w")

        file.write(f"{saved = }\ntimestamp = {activities[0][1] + weeks * 7*24*h}\nactivities = [ \n")
        for i in activities: file.write(f"\t{i},\n")
        file.write("]\n")

        file.close()

# error cheking
if saved == False:
    print(f"Предыдущая сессия была прервана: {activities[-1][0]} ({activities[-1][2]})")
    input(f"Добавление времени: {C}+{timedelta(0, int(time.time() - timestamp))}{W}\n")
    
    timestamp = time.time()
    data_save()

def stages_formatter(stages, verb=0):
    form =  ["этапа", "этапов", "этапов"] if verb else ["этап", "этапа", "этапов"]

    if int(str(stages)[-1]) == 1 and stages != 11: 
        return f"{stages} {form[0]}"
    
    if 1 <= int(str(stages)[-1]) <= 4 and (stages < 10 or stages > 20):
        return f"{stages} {form[1]}"
    
    else:
        return f"{stages} {form[2]}"

def analytics():
    sum_all = timestamp - activities[0][1]
    print(f"Итоги {stages_formatter(len(activities)-1, 1)} ({C}{timedelta(0, round(sum_all))}{W})")

    if sum_all == 0: return

    # dict of times
    activities_times = {}
    for activity_name in ACTIVITIES: activities_times |= {activity_name: []}
    
    for i, activity in enumerate(activities):
        pivot = activities[i+1][1] if i < len(activities) - 1 else timestamp
        activities_times[activity[0]].append(pivot - activity[1])

    # analyze all data
    for activity_name in ACTIVITIES:
        activity_time = sum(activities_times[activity_name])
        if activity_time == 0: continue

        activity_percentage = activity_time/sum_all * 100
        activity_counter = len(activities_times[activity_name])
        activity_mean = activity_time / activity_counter

        print(f"{activity_name} ({stages_formatter(activity_counter)}) ({round(activity_percentage, 2)}%)")
        print(f"Всего: {C}{timedelta(0, round(activity_time))}{W}")
        print(f"В среднем {C}{timedelta(0, round(activity_mean))}{W} за этап\n")

while True:
    os.system("clear")
    activity = len(activities) + 1

    stageline = f"Этап {M}{activity}{W}, ({datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')}) "

    if len(activities):
        stageline += f"({C}{timedelta(0, round(timestamp - activities[-1][1]))}{W})"

    print(stageline)
    print("Выбор занятия:")

    for i, name in enumerate(ACTIVITIES):
        print(f"{G}{i+1}{W}: {name}")

    print()

    for i, name in enumerate([
        "Завершить сессию", 
        "Удалить последнее занятие", 
        "Изменить время последнего занятия", 
        "Добавить подпись к последнему занятию"
    ]):
        print(f"{G}{'edci'[i]}{W}: {name}")
    
    session_id = input("\nНомер занятия: ")

    if session_id.isdigit(): session_id = int(session_id)
    elif session_id in ('e', 'd', 'c', 'i'): session_id = len(ACTIVITIES) + "edci".index(session_id) + 1
    else: session_id = 0
        
    print()

    # make new session
    if 1 <= session_id <= len(ACTIVITIES):
        activity_name = list(ACTIVITIES.keys())[session_id-1]

        # if activity repeat
        if len(activities) > 0 and activity_name == activities[-1][0]:
            print(f"Продолжение предудущей сессии -> {activities[-1][0]} ({activities[-1][2]})")

        else:
            note = ''
            if activity_name == 'Другое': note = input("Подпись: ") or 'Магазин'

            activities.append([
                f"{activity_name}", 
                timestamp,
                f"{datetime.fromtimestamp(timestamp).strftime('%d.%m.%Y %H:%M:%S')}",
                note
            ])
        
        data_save(saved=False)
        input(f"<< {activity_name} >>")

        timestamp = time.time()
    
    # end sesstion
    if session_id == len(ACTIVITIES) + 1:
        data_save()
        analytics()
        exit()

    # delete last activity
    if session_id == len(ACTIVITIES) + 2 and len(activities):
        print(f"Удалить: {activities[-1][0]} ({activities[-1][2]})?")
        if input("y/n: ").lower() == "y":
            activities.pop()
        else:
            input(f"\n{R}Удаление отменено{W}")

    # change last activity time
    if session_id == len(ACTIVITIES) + 3:
        activity_name = activities[-1][0]
        activity_start_time = activities[-1][2]

        activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))

        try: 
            print(f"Изменение предыдущего занятия\n{activity_name} ({activity_start_time}) {C}{activity_lasts}{W}")
            activities[-1][1] += eval(input("\nОтнять секунд: "))
            activities[-1][2] = (datetime.fromtimestamp(activities[-1][1])).strftime('%d.%m.%Y %H:%M:%S')
        except: 
            input(f"\n{R}Ошибка ввода{W}")

    # add a note
    if session_id == len(ACTIVITIES) + 4:
        activity_name = activities[-1][0]
        activity_start_time = activities[-1][2]
        activity_lasts = timedelta(0, round(timestamp - activities[-1][1]))

        print(f"Добавление подписи к предыдущему занятию\n{activity_name} ({activity_start_time}) {C}{activity_lasts}{W}")
        note = input("\nПодпись: ")

        activities[-1][-1] = note

    data_save()
