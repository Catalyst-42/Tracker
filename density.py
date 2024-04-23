import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.ticker import PercentFormatter, MultipleLocator

import save
from setup import setup

from utils import w
from utils import normalize_color
from utils import generate_activites_times

ARGS, ACTIVITIES = setup("density")
activities_times = generate_activites_times(save.activities, save.timestamp)

bars = {}
period_times = {activity_name: 0 for activity_name in ACTIVITIES}

# Create plot canvas
fig, axs = plt.subplot_mosaic(
    [["average"]],
    figsize=(ARGS["PLOT_WIDTH"], ARGS["PLOT_HEIGHT"])
)

fig.canvas.manager.set_window_title("Плотность занятий")
ax = list(axs.items())

def construct_bars(week):
    offset = 0
    bars[week] = {}
    
    # Create bars for each activity
    for activity_name in period_times:
        percentage = period_times[activity_name] / period
        bars[week][activity_name] = percentage
        
        if activity_name == ARGS["VOID"] or percentage == 0: 
            continue
        
        ax[0][1].bar(
            x=week,
            height=percentage,
            bottom=offset,
            width=1,
            edgecolor="black",
            color=normalize_color(ACTIVITIES[activity_name]),
            linewidth=.5
        )

        if period_times[activity_name] >= ARGS["LABEL_TRESHOLD"] * period:
            ax[0][1].text(
                x=week,
                y=period_times[activity_name]/period/2 + offset,
                s=f"{round(period_times[activity_name]/period * 100, 1)}%",
                va="center",
                ha="center",
                rotation="vertical",
                clip_on=True
            )

        offset += percentage

# Process all activities and add them to plot
stage = 1
period = w * (stage if ARGS["CUMULATIVE"] else 1)

for i in range(len(save.activities)):
    activity = save.activities[i]
    
    total_time = sum([period_times[theme] for theme in period_times])
    this_activity_time = activities_times[activity[0]].pop(0)
    
    while total_time + this_activity_time >= period:
        period_times[activity[0]] += period - total_time
        this_activity_time -= period - total_time
        
        construct_bars(stage)

        if not ARGS["CUMULATIVE"]:
            for activity_name in period_times:
                period_times[activity_name] = 0
        
        stage += 1
        period = w * (stage if ARGS["CUMULATIVE"] else 1)
        total_time = sum([period_times[theme] for theme in period_times])
        
    else:
        period_times[activity[0]] += this_activity_time

else:
    # Create data for last not full week
    if (total_time + this_activity_time) % w != 0:
        construct_bars(stage)
        stage += 1

# Form legend
if ARGS["SHOW_LEGEND"]:
    legend_elements = []
    
    for activity_name in ACTIVITIES:
        if activity_name in activities_times and activity_name != ARGS["VOID"]:
            legend_elements.append(
                Patch(
                    facecolor=normalize_color(ACTIVITIES[activity_name]),
                    edgecolor="black",
                    linewidth=.5,
                    label=activity_name
                )
            )
    
    ax[0][1].legend(handles=legend_elements, ncol=ARGS["LEGEND_COLUMNS"])

def format_coord(x, y):
    # Form bar info
    bar_info = ""
    if 0.5 <= round(x) <= len(bars):
        percentage = 0
        for activity_name in bars[round(x)]:
            activity_percentage = bars[round(x)][activity_name]
            
            if percentage <= y <= percentage + activity_percentage:
                bar_info = (
                    f"{activity_name} "
                    f"({round(activity_percentage * 100, 1)}%, "
                    f"{round(activity_percentage * 7*24, 1)}ч/н, "
                    f"{round(activity_percentage * 24, 1)}ч/д)\n"
                )
                break
            
            percentage += bars[round(x)][activity_name]
    
    # Form position info
    position_info = (
        f"x={round(x)} неделя, "
        f"y={round(y * 100, 1)}% "
        f"({round(y * 24*7, 1)}ч/н, "
        f"{round(y * 24, 1)}ч/д)"
    )
    
    return bar_info + position_info

percentages_max = round(
    max(
        [sum(bars[i].values()) - (bars[i][ARGS["VOID"]] if ARGS["HIDE_VOID"] else 0)
        for i in range(1, stage)]
    ),
    1 + 2
)

ax[0][1].format_coord = format_coord

ax[0][1].set_xticks([i for i in range(1, stage)], [i for i in range(1, stage)])
ax[0][1].set_xlim(.5, stage - .5)

ax[0][1].set_ylim(0, percentages_max)
ax[0][1].yaxis.set_major_formatter(PercentFormatter(1.0))
ax[0][1].yaxis.set_major_locator(MultipleLocator(percentages_max / 10))

plt.tight_layout()

if ARGS["IMAGE"]:
    plt.savefig(f"density.png", bbox_inches="tight")

if not ARGS["SILENT"]:
    plt.show()
