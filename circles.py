from math import *
from datetime import datetime

import numpy
from PIL import Image

import save
from constants import *

# Check if there are colors for all activities
for activity in save.activities:
    if activity not in ACTIVITIES:
        print(f"Занятия {B}{activity}{W} нет в списке активностей!")

if set(save.activities.keys()) != set(ACTIVITIES.keys()):
    exit()

# Make circle
data = numpy.zeros((MAX_X, MAX_Y, 3), dtype=numpy.uint8)
data[:][:] = COLOR_BG
x_prev = 0
days = 0

for x in save.activities_log:
    activity, x = x
    x = (datetime.strptime(x, "%H:%M:%S") - datetime.strptime("00:00:00", "%H:%M:%S")).total_seconds() + 1
    x /= h

    if x < x_prev: days += 1
    x_prev = x

    y = round(cos(pi * x / 12)*(RADIUS + days//7) - MAX_Y//2)
    x = round(sin(pi * x / 12)*(RADIUS + days//7) + MAX_X//2)
    data[x][y] = ACTIVITIES[activity]

print(days/7, 'weeks')

image = Image.fromarray(data)
image = image.transpose(Image.Transpose.ROTATE_90)
image = image.resize((RESIZE_TO[0], RESIZE_TO[1]), resample=Image.Resampling.BOX)
image.save('image.png')
image.show()
