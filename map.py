from datetime import datetime

import matplotlib.pyplot as plt
from matplotlib.patches import Patch

import save
from setup import setup

from utils import m, h, d, w
from utils import generate_activites_times
from utils import normalize_color
from utils import weekdays, months

ARGS, ACTIVITIES = setup("map")
activities_times = generate_activites_times(save.activities, save.timestamp)

# Create plot canvas
fig, axs = plt.subplot_mosaic(
    [["main"]],
    figsize=(ARGS["PLOT_WIDTH"], ARGS["PLOT_HEIGHT"]), 
)

fig.canvas.manager.set_window_title("Карта сохранения")
ax = list(axs.items())

all_experiment_time = sum([sum(activities_times[i]) for i in activities_times])
save_activities = set([i[0] for i in save.activities])

average_day = {
    activity_name: sum(activities_times[activity_name]) for activity_name in ACTIVITIES 
    if activity_name != ARGS["VOID"] and activity_name in save_activities
}

def bar_constructor(x, y):
    global offset

    if activity[0] != ARGS["VOID"]:
        ax[0][1].bar(
            x=x,
            bottom=offset,
            width=1,
            height=y,
            linewidth=.5,
            color=normalize_color(ACTIVITIES[activity[0]])
        )

    offset += y

# Generate all parts and add it to plot
experiment_start_time = save.activities[0][1]
offset = experiment_start_time % d + ARGS["UTC_OFFSET"]
days = 1

for activity in save.activities:
    # Create one bar
    if activities_times[activity[0]][0] <= d - offset:
        bar_constructor(days, activities_times[activity[0]][0])

    else:
        to_distribute = activities_times[activity[0]][0]
        to_distribute -= d - offset
        bar_constructor(days, d - offset)

        # Create bars, separated by days
        while to_distribute != 0:
            days += 1
            offset = 0

            if to_distribute >= d:
                bar_constructor(days, d)
                to_distribute -= d
            else:
                bar_constructor(days, to_distribute)
                to_distribute = 0

    activities_times[activity[0]].pop(0)

if ARGS["SHOW_LEGEND"]:
    legend_elements = [
        Patch(
            facecolor=normalize_color(ACTIVITIES[i]),
            edgecolor="black",
            linewidth=.5,
            label=i
        ) for i in average_day if i != ARGS["VOID"]
    ]
    
    ax[0][1].legend(handles=legend_elements, ncol=ARGS["LEGEND_COLUMNS"], loc="lower left")

start_day = datetime.fromtimestamp(save.activities[0][1]).weekday()
start_hour = experiment_start_time%(d) + ARGS["UTC_OFFSET"]

def format_coord(x, y):
    x = int(x-.5)
    y = round(y/h) if round(y/h, 1) == round(y/h) else round(y/h, 1)
    
    selected_time = x*d + y*h + experiment_start_time - start_hour
    
    # Form bar info
    bar_info = ""
    for k, i in enumerate(save.activities):
        if i[1] >= selected_time or not save.activities[0][1] <= selected_time <= save.timestamp: break
        pivot = save.timestamp if len(save.activities)-1 == k else save.activities[k+1][1]
        
        bar_info = f"{i[0]}"
        bar_info += f" ({i[-1]})" if i[-1] else ""
        bar_info += (
            f" ({round((pivot - i[1]) / h, 1)}ч)\n" if (pivot - i[1]) / h >= 1 else
            f" ({round((pivot - i[1]) / m, 1)}м)\n"
        )
        
    # Form position info
    month = months[datetime.fromtimestamp(selected_time).month - 1]
    day = datetime.fromtimestamp(selected_time).day
    week = round((selected_time - experiment_start_time) // w + 1)
    
    position_info = (
        f"x={weekdays[(x+start_day)%7]}, {y=}ч "
        f"({day} {month}, {week} неделя)"
    )
        
    return bar_info + position_info

ax[0][1].format_coord = format_coord

ax[0][1].set_xticks(range(1, days+1, 7), [(i+start_day) for i in range(1, days+1, 7)])
ax[0][1].set_xlim(.5, days + .5)
ax[0][1].xaxis.set_major_formatter(lambda x, _: int(x-.5)//7+1)

ax[0][1].set_yticks(range(0, d+1, d//10), [f"{i}%" for i in range(0, 101, 10)])
ax[0][1].set_ylim(0, d)
ax[0][1].yaxis.set_major_formatter(lambda y, _: f"{round(y/h) if round(y/h, 1) == round(y/h) else round(y/h, 1)}ч")

plt.tight_layout()

if ARGS["IMAGE"]:
    plt.savefig(f"map.png", bbox_inches="tight")

if not ARGS["SILENT"]:
    plt.show()
