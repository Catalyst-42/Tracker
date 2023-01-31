import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import save

from datetime import datetime
from matplotlib.patches import Patch
from constants import *

# Check if there are colors for all activities
heap = []
for activity in save.activities:
    if activity[0] not in ACTIVITIES and activity[0] not in heap:
        print(f"Занятия {B}{activity[0]}{W} нет в списке активностей!")
        heap.append(activity[0])

if len(heap): exit()
del heap

# dict of times
activities_times = {}
for activity_name in ACTIVITIES: activities_times |= {activity_name: []}

for i, activity in enumerate(save.activities):
    pivot = save.activities[i+1][1] if i < len(save.activities) - 1 else save.timestamp
    activities_times[activity[0]].append(pivot - activity[1])

# Because colors in matplotlib should be in 0-1 range
for activity in ACTIVITIES:
    ACTIVITIES[activity] = tuple([rgb/255 for rgb in ACTIVITIES[activity]])

AVERAGE_DAY = {}
for activity_name in ACTIVITIES:
    if activity_name == "Void": continue
    AVERAGE_DAY |= {activity_name: 0}

START_DAY = datetime.fromtimestamp(save.activities[0][1]).weekday()
EXPERIMENT_START_TIME = save.activities[0][1]
ALL_EXPERIMENT_TIME = sum([sum(activities_times[i]) for i in activities_times])

fig, axs = plt.subplot_mosaic(
    [["main", "average"]],
    figsize = (PLOT_START_WIDTH + ALL_EXPERIMENT_TIME//(24*h)*PLOT_WIDTH_STEP if FULL else PLOT_WIDTH, PLOT_HEIGTH), 
    gridspec_kw = {"width_ratios": [(ALL_EXPERIMENT_TIME//(24*h) + 2 if ALL_EXPERIMENT_TIME >= 48*h else 2) if FULL else 14, 1]}
)

fig.canvas.manager.set_window_title("Распределение времени")
if EXCLUDE_VOIDS and "Void" in ACTIVITIES: ALL_EXPERIMENT_TIME -= sum(activities_times["Void"])

# print hours and percentages
print(f"Всего: {round(ALL_EXPERIMENT_TIME / h, 1)}ч\n")
for activity in activities_times:
    if activity == "Void": continue
    
    AVERAGE_DAY[activity] = sum(activities_times[activity])
    print(f"{activity}: {round(AVERAGE_DAY[activity]/h,2)}ч ({round(AVERAGE_DAY[activity]/ALL_EXPERIMENT_TIME * 100, 1)}%)")

ax = list(axs.items())
x = [1]
offset = 0
days = 1

# First plot - distribution for all days
def bar_constructor(x, y):
    global offset

    offset += y
    if activity[0] == "Void": return

    ax[0][1].bar(x, y, width=1, bottom=offset-y, edgecolor="black", linewidth=.5, color=ACTIVITIES[activity[0]], label=activity[-1])
    if y >= .9*h:
        ax[0][1].text(x, (y/2+offset-y), f"{round(y/h) if round(y/h, 1) == round(y/h) else round(y/h, 1)}ч", va="center", ha="center", clip_on=True)

# generate all parts and add it to plot
for i in range(len(save.activities)):
    activity = save.activities[i]

    if i != len(save.activities) - 1: 
        next_activity_time = datetime.strptime(save.activities[i+1][2], "%d.%m.%Y %H:%M:%S")
    else: 
        next_activity_time = datetime.utcfromtimestamp(save.timestamp)
    
    this_activity_time = datetime.strptime(activity[2], "%d.%m.%Y %H:%M:%S")
    
    activity_max_time = datetime.strptime(activity[2][:10] + " 23:59:59", "%d.%m.%Y %H:%M:%S")
    activity_min_time = datetime.strptime(activity[2][:10] + " 00:00:00", "%d.%m.%Y %H:%M:%S")
    
    # first bar
    if not i:
        offset = (this_activity_time - activity_min_time).total_seconds()

    # create one bar
    if activities_times[activity[0]][0] <= 24*h - offset:
        bar_constructor(days, activities_times[activity[0]][0])

    else:
        to_distribute = activities_times[activity[0]][0]
        to_distribute -= 24*h - offset
        bar_constructor(days, 24*h - offset)

        # create bars, separated by days
        while to_distribute != 0:
            x.append(len(x)+1)
            days += 1
            offset = 0

            if to_distribute >= 24*h:
                bar_constructor(days, 24*h)
                to_distribute -= 24*h
            else:
                bar_constructor(days, to_distribute)
                to_distribute = 0

    activities_times[activity[0]].pop(0)

ax[0][1].set_xticks(x, [DAYS_OF_WEEK[(i+START_DAY)%7] for i in range(len(x))])
ax[0][1].set_xlim(0.5, len(x) + .5 if FULL else 14.5)
ax[0][1].invert_yaxis()
ax[0][1].set_ylim(0, 24*h)
ax[0][1].set_yticks([i*864 for i in range(0, 101, 10)], [f"{i}%" for i in range(0, 101, 10)])

ax[0][1].xaxis.set_major_formatter(lambda x, _: DAYS_OF_WEEK[(int(x-.5)+START_DAY)%7])
ax[0][1].yaxis.set_major_formatter(lambda y, _: f"{round(y/h) if round(y/h, 1) == round(y/h) else round(y/h, 1)}ч")

def format_coord(y, x):
    x = round(x/h) if round(x/h, 1) == round(x/h) else round(x/h, 1)
    y = (int(y-.5))

    timestamp = y*24*h + x*h + EXPERIMENT_START_TIME - EXPERIMENT_START_TIME%(24*h) - UTC_OFFSET
    note = ''

    week = f"({round((timestamp - EXPERIMENT_START_TIME) // (7*24*h) + 1)} неделя)"
    if not save.activities[0][1] <= timestamp <= save.timestamp: week = ''

    for i in save.activities:
        if i[1] >= timestamp or not save.activities[0][1] <= timestamp <= save.timestamp: break
        note = i[-1]

    if note: return f"Подпись: {note}\nx={DAYS_OF_WEEK[(y+START_DAY)%7]} {week}, y={x}ч"
    else: return f"\nx={DAYS_OF_WEEK[(y+START_DAY)%7]} {week}, y={x}ч"

ax[0][1].format_coord = format_coord

legend_elements = [*[Patch(facecolor=ACTIVITIES[i], edgecolor="black", linewidth=.5, label=i) for i in AVERAGE_DAY]]
ax[0][1].legend(handles=legend_elements, ncol=1, loc="lower left")

# Second plot - Average time
offset = 0

for activity in AVERAGE_DAY:
    ax[1][1].bar(1, AVERAGE_DAY[activity], width=1, edgecolor="black", color=ACTIVITIES[activity], linewidth=.5, bottom=offset, label=activity)

    if AVERAGE_DAY[activity] >= ALL_EXPERIMENT_TIME * 0.05:
        ax[1][1].text(1, (AVERAGE_DAY[activity]/2+offset), f"{round(AVERAGE_DAY[activity]/ALL_EXPERIMENT_TIME*100, 1)}%", va="center", ha="center", clip_on=True)

    offset += AVERAGE_DAY[activity]

ax[1][1].set_xticks((1,), ("AV",))
ax[1][1].set_xlim(.5, 1.5)
ax[1][1].invert_yaxis()
ax[1][1].set_ylim(0, ALL_EXPERIMENT_TIME)
ax[1][1].set_yticks([i*ALL_EXPERIMENT_TIME/100 for i in range(0, 101, 10)], [f"{i}%" for i in range(0, 101, 10)])

ax[1][1].xaxis.set_major_formatter(lambda *_: "AV")
ax[1][1].yaxis.set_major_formatter(mtick.PercentFormatter(ALL_EXPERIMENT_TIME))
ax[1][1].yaxis.tick_right()

plt.tight_layout()
plt.savefig(f"plot.png", bbox_inches="tight")

plt.show()
