# Time
s = 1
m = 60
h = 3600
DAYS_OF_WEEK = ('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС')

# Experiment values
START_DAY = DAYS_OF_WEEK.index('ВС')
ACTIVITIES = {
    "Сон": (31, 119, 180),
    "Отдых": (255, 127, 14),
    "Пары": (44, 160, 44),
    "Метро": (214, 39, 40),
    "Домашка": (149, 103, 189),
    "Магазин": (140, 86, 75),
    # Should be expanded if you have created more activities
}

AVERAGE_DAY = {}
for activity_name in ACTIVITIES:
    AVERAGE_DAY |= {activity_name: [0]}

# Circles values
RADIUS = 32
MAX_X, MAX_Y = 128, 128
RESIZE_TO = (MAX_X*4, MAX_Y*4)
COLOR_BG = (21, 23, 32)

# Terminal colors
W = "\033[0m"  # white
B = "\033[30m" # blue
R = "\033[31m" # red
G = "\033[32m" # green
Y = "\033[33m" # yellow
M = "\033[35m" # magenta
C = "\033[36m" # cyan
