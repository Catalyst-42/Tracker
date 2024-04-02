# Time
s = 1
m = 60 * s
h = 60 * m
d = 24 * h
w = 7 * d

# Colors
white = "\033[0m"
red = "\033[31m"
green = "\033[32m"
yellow = "\033[33m"
blue = "\033[34m"
magenta = "\033[35m"
cyan = "\033[36m"

# Days
weekdays = (
    "Пн",
    "Вт",
    "Ср",
    "Чт",
    "Пт",
    "Сб",
    "Вс"
)

months = (
    "Января",
    "Февраля",
    "Марта",
    "Апреля",
    "Мая",
    "Июня",
    "Июля",
    "Августа",
    "Сентября",
    "Октября",
    "Ноября",
    "Декабря"
)

def color(text, color):
    return f"{color}{text}{white}"

def normalize_color(activity):
    color = tuple([rgb/255 for rgb in activity])
    
    return color

def generate_activites_times(activities, timestamp):
    save_activities_names = set([i[0] for i in activities])
    activities_times = {activity_name: [] for activity_name in save_activities_names}

    for i, activity in enumerate(activities):
        pivot = activities[i+1][1] if i < len(activities) - 1 else timestamp
        activity_time = pivot - activity[1]
        
        # print(timedelta(activity_time))
        activities_times[activity[0]].append(activity_time)
        
    return activities_times

def stages_formatter(stages, verb=0):
    if verb:
        form = ["этапа", "этапов", "этапов"]
    else:
        form = ["этап", "этапа", "этапов"]
        
    last_digit = int(str(stages)[-1])
    last_2_digits = int(str(stages)[-2:])

    if last_digit == 1 and last_2_digits != 11:
        return f"{stages} {form[0]}"
    
    if 1 <= last_digit <= 4 and (last_2_digits < 10 or last_2_digits > 20):
        return f"{stages} {form[1]}"
    
    return f"{stages} {form[2]}"

# def delta(time, cap=d):    
#     for postfix, name in ((w, 'н'), (d, 'д'), (h, 'ч'), (m, 'м'), (s, 'с')):
#         if time >= postfix and postfix <= cap:
#             time = time / postfix
#             return f"{round(time) if round(time, 1) == round(time) else round(time, 1)}{name}"

def timedelta(time):
    time = int(time)
    
    if time < d:
        weeks = ""
    else:
        weeks = f"{time // d}д"
        time -= d * (time // d)
    
        if time == 0:
            return weeks
        else:
            weeks += " "
    
    clock = []
    for period in (h, m, s):
        clock.append(f"{time // period:02}")
        time -= period * (time // period)
    
    return weeks + ':'.join(clock)
