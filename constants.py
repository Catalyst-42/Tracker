from time import timezone
from platform import platform

# Time
s = 1
m = 60
h = 3600

UTC_OFFSET = -timezone
DAYS_OF_WEEK = ('ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС')

# Tracker settings
CLEAR = "cls" if platform() == "Windows" else "clear"
EXCLUDE_VOIDS = True # exclude void time from total time (and AV plot)
ACTIVITIES = {
    "Сон": (31, 119, 180),
    "Отдых": (255, 127, 14),
    "Пары": (44, 160, 44),
    "Метро": (214, 39, 40),
    "Домашка": (149, 103, 189),
    "Другое": (140, 86, 75),
    # "Void": (0, 0, 0) # empty time
    
    # Activity name: activity color (for plots, rgb)
    # Can be expanded with custom activities
    # Order determines plot of average day
}

# Plot settings
FULL = True # display the entire plot or frame it by 2 weeks
PLOT_WIDTH = 9
PLOT_HEIGTH = 5.7

PLOT_START_HEIGTH = 2.2
PLOT_START_WIDTH = 3.5

PLOT_HEIGTH_STEP = 0.25
PLOT_WIDTH_STEP = 0.45

PLOT_START_DAY_OFFSET = 0.0
LABELS_IN_ROW = len(ACTIVITIES)

# Circles settings
RADIUS = 32
MAX_X, MAX_Y = 128, 128
RESIZE_TO = (MAX_X*4, MAX_Y*4)
COLOR_BG = (21, 23, 32)

# Terminal colors
W = "\033[0m"  # white
R = "\033[31m" # red
G = "\033[32m" # green
Y = "\033[33m" # yellow
B = "\033[34m" # blue
M = "\033[35m" # magenta
C = "\033[36m" # cyan
