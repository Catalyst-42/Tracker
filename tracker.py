import time
import os

from datetime import datetime, timedelta

from constants import *


timestamp = time.time()
activity = 1
displaced_time = 0
activities_log = []

activities = {}

for activity_name in ACTIVITIES:
    activities |= {activity_name: []}

open("save.py", "a")

from save import *

def data_save():
    file = open("save.py", "w")
    file.write(f"{timestamp=} \n{activity=} \n{displaced_time=} \n{activities_log=} \n{activities=} ")
    file.close()

# error cheking
if sum(len(activities[activity]) for activity in activities) < len(activities_log):
    print(f"Обнаружена ошибка в данных: {activities_log[-1][0]} ({activities_log[-1][1]})")
    input(f"Добавление времени: {C}+{timedelta(seconds=int(time.time() - timestamp))}{W}\n")

    activity_name = activities_log[-1][0] 
    activities[activity_name].append(time.time() - timestamp)
    
    activity += 1
    timestamp = time.time()
    data_save()

# stage formatter
def stages_formatter(stages, verb=0):
    form = ["этап", "этапа", "этапов"]

    if verb: 
        form = ["этапа", "этапов", "этапов"]

    if int(str(stages)[-1]) == 1 and stages != 11: 
        return f"{stages} {form[0]}"

    if 1 <= int(str(stages)[-1]) <= 4 and (stages < 10 or stages > 20):
        return f"{stages} {form[1]}"
    else:
        return f"{stages} {form[2]}"

# analytycs
def analytycs():
    sum_all = sum(sum(activities[activity]) for activity in activities)
    print(f"Итоги {stages_formatter(activity-1, 1)} ({C}{timedelta(seconds=round(sum_all))}{W})")

    if sum_all == 0: return

    for activity_name in activities:
        activity_time = sum(activities[activity_name])
        if activity_time == 0: continue

        activity_percentage = activity_time/sum_all * 100
        activity_counter = len(activities[activity_name])
        activity_mean = activity_time / activity_counter

        print(f"{activity_name} ({stages_formatter(activity_counter)}) ({round(activity_percentage, 2)}%)")
        print(f"Всего: {C}{timedelta(seconds=round(activity_time))}{W}")
        print(f"В среднем {C}{timedelta(seconds=round(activity_mean))}{W} за этап\n")

# main loop
while True:
    os.system("clear")

    stageline = f"Этап {M}{activity}{W}, ({datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')}) "

    if len(activities_log):
        stageline += f"({C}{timedelta(seconds=round(activities[activities_log[-1][0]][-1]))}{W})"

    print(stageline)
    print("Выбор занятия:")

    for i, name in enumerate(activities):
        print(f"{G}{i+1}{W}: {name}")

    print()

    for i, name in enumerate(["Завершить сессию", "Удалить последнее занятие", "Изменить время последнего занятия", "Добавить новое занятие"]):
        print(f"{G}{'edca'[i]}{W}: {name}")
    
    session_id = input("\nНомер занятия: ")

    if session_id.isdigit(): 
        session_id = int(session_id)
    elif session_id in ("e", "d", "c", "a"):
        session_id = len(activities) + "edca".index(session_id) + 1
    else:
        session_id = 0
        
    print()

    # make new session
    if 1 <= session_id <= len(activities):
        activity_name = list(activities.keys())[session_id-1]
        activity_repeat = False

        # activity repeat
        if len(activities_log) > 0 and activity_name == activities_log[-1][0]:
            print(f"Продолжение предудущей сессии -> {activities_log[-1][0]} ({activities_log[-1][1]})")
            activity_repeat = True

        # displaced time check
        if displaced_time:
            timestamp -= displaced_time
            print(f"Обнаружено нераспределённое время ({C}{timedelta(seconds=round(displaced_time))}{W})")
            print(f"Изменение текущего занятия -> {activity_name} ({datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')})")
            
            displaced_time = 0

        # create new activity if it"s not repeat
        if not activity_repeat:
            activities_log.append((f"{activity_name}", f"{datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')}"))
        
        data_save()
        input(f"<< {activity_name} >>")

        # add time to activity
        if activity_repeat:
            activities[activity_name][-1] += time.time() - timestamp
        else:
            activities[activity_name].append(time.time() - timestamp)
            activity += 1

        timestamp = time.time()
    
    # end sesstion
    if session_id == len(activities) + 1:
        data_save()
        analytycs()
        exit()

    # delete last activity
    if session_id == len(activities) + 2 and len(activities_log):
        print(f"Удалить: {activities_log[-1][0]} ({activities_log[-1][1]})?")
        if input("y/n: ").lower() == "y":
            displaced_time = activities[activities_log.pop()[0]].pop()
            activity -= 1
        else:
            input(f"\n{R}Удаление отменено{W}")

    # change last activity time
    if session_id == len(activities) + 3:
        activity_name = activities_log[-1][0]
        activity_start_time = activities_log[-1][1]

        activity_lasts = timedelta(seconds=round(activities[activity_name][-1]))

        try: 
            displaced_time += eval(
                input(f"{activity_name} ({activity_start_time}) {C}{activity_lasts}{W} \nОтнять секунд: ")
            )
        except: 
            input(f"\n{R}Ошибка ввода{W}")
        activities[activity_name][-1] -= displaced_time

    if session_id == len(activities) + 4:
        activity_name = input("Название нового занятия: ")
        if activity_name not in activities and activity_name != "":
            activities = activities | {activity_name: []}

    data_save()
