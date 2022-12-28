from math import *
from datetime import datetime

import numpy
from PIL import Image

import save
from constants import *

# Check if there are colors for all activities
not_in = []
for activity in save.activities:
    if activity[0] not in ACTIVITIES and activity[0] not in not_in:
        print(f"Занятия {B}{activity[0]}{W} нет в списке активностей!")
        not_in.append(activity[0])

if len(not_in): exit()
del not_in

# dict of times
activities_times = {}
for activity_name in ACTIVITIES: activities_times |= {activity_name: []}

for i, activity in enumerate(save.activities):
    pivot = save.activities[i+1][1] if i < len(save.activities) - 1 else save.timestamp
    activities_times[activity[0]].append(pivot - activity[1])

# Make circle
image = numpy.zeros((MAX_X, MAX_Y, 3), dtype=numpy.uint8)
image[:][:] = COLOR_BG
data_start = datetime.strptime(save.activities[0][2], "%d.%m.%Y %H:%M:%S")
days = 0

for i, x in enumerate(save.activities):
    activity, _, data, _ = x
    
    x = (datetime.strptime(data, "%d.%m.%Y %H:%M:%S") - datetime.strptime(data[:10] + " 00:00:00", "%d.%m.%Y %H:%M:%S"))
    x = (x.total_seconds() + 1 ) / h
    
    if i != len(save.activities) - 1: 
        days = (datetime.strptime(data, "%d.%m.%Y %H:%M:%S") - data_start).days
    else: 
        days = (datetime.utcfromtimestamp(save.timestamp) - data_start).days

    y = round(cos(pi * x / 12)*(RADIUS + days//7) - MAX_Y//2)
    x = round(sin(pi * x / 12)*(RADIUS + days//7) + MAX_X//2)
    image[x][y] = ACTIVITIES[activity]

print('weeks:', days/7)

image = Image.fromarray(image)
image = image.transpose(Image.Transpose.ROTATE_90)
image = image.resize((RESIZE_TO[0], RESIZE_TO[1]), resample=Image.Resampling.BOX)
image.save('image.png')
image.show()
