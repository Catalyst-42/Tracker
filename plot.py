from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.patches import Patch

from save import *
from constants import ACTIVITIES, AVERAGE_DAY, DAYS_OF_WEEK, START_DAY
from constants import h, m, s

# Because colors in matplotlib should be in 0-1 range
for activity in ACTIVITIES:
    ACTIVITIES[activity] = [rgb/255 for rgb in ACTIVITIES[activity]]
ALL_EXPERIMENT_TIME = sum([sum(activities[i]) for i in activities])

for activity in activities:
    AVERAGE_DAY[activity] = sum(activities[activity])
    print(f'{activity}: {round(AVERAGE_DAY[activity]/h,2)}ч')

fig, axs = plt.subplot_mosaic([['main'],
                            ['average']], figsize=(9, 1+ALL_EXPERIMENT_TIME//(24*h)*0.25), gridspec_kw={'height_ratios': [ALL_EXPERIMENT_TIME//(24*h), 1]})
fig.canvas.manager.set_window_title('Распределение времени')
ax = list(axs.items())
x = [1]
offset = 0
days = 1

# First plot - distribution for all days
def bar_constructor(x, y):
    global offset
    ax[0][1].barh(x, y, left=offset, height=1, edgecolor='black', linewidth=.5, color=ACTIVITIES[activity[0]])
    if y >= .9*h:
        ax[0][1].text((y/2+offset), x, f'{round(y/h) if round(y/h, 1) == round(y/h) else round(y/h, 1)}ч', va='center', ha='center')
    offset += y

for i in range(len(activities_log)):
    activity = activities_log[i]
    if i != len(activities_log) - 1: next_activity_time = datetime.strptime(activities_log[i+1][1], "%H:%M:%S")
    this_activity_time = datetime.strptime(activity[1], "%H:%M:%S")
    
    activity_max_time = datetime.strptime("23:59:59", "%H:%M:%S")
    activity_min_time = datetime.strptime('00:00:00', "%H:%M:%S")

    if not i: offset = (this_activity_time - activity_min_time).total_seconds() + 1

    if i == len(activities_log) - 1 or next_activity_time > this_activity_time:
        bar_constructor(days, activities[activity[0]][0])
        activities[activity[0]].pop(0)

    else:
        bar_constructor(days, (activity_max_time - this_activity_time).total_seconds() + 1)

        x.append(len(x)+1)
        days += 1
        offset = 0

        if i != len(activities_log) - 1:
            bar_constructor(days, (next_activity_time - activity_min_time).total_seconds())
        activities[activity[0]].pop(0)

ax[0][1].set_yticks(x, [DAYS_OF_WEEK[(i+START_DAY)%7] for i in range(len(x))])
ax[0][1].set_ylim(-.2, len(x) + .5)
ax[0][1].invert_yaxis()
ax[0][1].set_xlim(0, 24*h)
ax[0][1].set_xticks([i*864 for i in range(0, 101, 10)], [f'{i}%' for i in range(0, 101, 10)])

ax[0][1].yaxis.set_major_formatter(lambda x, _: DAYS_OF_WEEK[(int(x-.5)+START_DAY)%7])
ax[0][1].xaxis.set_major_formatter(lambda x, _: f'{round(x/h) if round(x/h, 1) == round(x/h) else round(x/h, 1)}ч')

legend_elements = [*[Patch(facecolor=ACTIVITIES[i], edgecolor='black', linewidth=.5, label=i) for i in AVERAGE_DAY]]
ax[0][1].legend(handles=legend_elements, ncol=len(AVERAGE_DAY), loc='upper left')

# Second plot - Average time
offset = 0
for activity in list(AVERAGE_DAY.keys()):
    ax[1][1].barh(1, AVERAGE_DAY[activity], height=1, edgecolor='black', linewidth=.5, left=offset, label=activity)
    if AVERAGE_DAY[activity] >= ALL_EXPERIMENT_TIME * 0.05:
        ax[1][1].text((AVERAGE_DAY[activity]/2+offset), 1, f'{round(AVERAGE_DAY[activity]/ALL_EXPERIMENT_TIME*100, 1)}%', va='center', ha='center')
    offset += AVERAGE_DAY[activity]

ax[1][1].set_yticks([1], ['AV'])
ax[1][1].set_ylim(.5, 1.5)
ax[1][1].invert_yaxis()
ax[1][1].set_xlim(0, ALL_EXPERIMENT_TIME)
ax[1][1].set_xticks([i*ALL_EXPERIMENT_TIME/100 for i in range(0, 101, 10)], [f'{i}%' for i in range(0, 101, 10)])

ax[1][1].yaxis.set_major_formatter(lambda x, _: "AV")
ax[1][1].xaxis.set_major_formatter(mtick.PercentFormatter(ALL_EXPERIMENT_TIME))

plt.tight_layout()
plt.savefig(f'day_{days}.png', bbox_inches='tight')
plt.show()
