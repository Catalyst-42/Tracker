from math import *
from datetime import datetime

import numpy
from PIL import Image

import save

s = 1
m = 60 * s
h = 60 * m

R = 32
MAX_X, MAX_Y = 128, 128
RESIZE_TO = (MAX_X * 4, MAX_Y * 4)

COLORS = {
    "Сон": (31, 119, 180),
    "Отдых": (255, 127, 14),
    "Пары": (44, 160, 44),
    "Метро": (214, 39, 40),
    "Домашка": (149, 103, 189),
    "Магазин": (140, 86, 75),
    "Test": (255, 255, 255),
}

data = numpy.zeros((MAX_X, MAX_Y, 3), dtype=numpy.uint8)
data[:][:] = (21, 23, 32)
x_prev = 0
days = 0

# test = []
# for hrs in range(0, 24):
#     test.append(['Test', f'{hrs}:00:00'])
# save.activities_log = test #+ save.activities_log

for x in save.activities_log:
    color, x = x
    x = (datetime.strptime(x, "%H:%M:%S") - datetime.strptime("00:00:00", "%H:%M:%S")).total_seconds() + 1
    x /= h

    if x < x_prev: days += 1
    x_prev = x

    y = round(cos(pi * x / 12) * (R + days // 7) - MAX_Y // 2)
    x = round(sin(pi * x / 12) * (R + days // 7) + MAX_X // 2)
    data[x][y] = COLORS[color]

print(days / 7, 'weeks')

image = Image.fromarray(data)
image = image.transpose(Image.ROTATE_90)
image = image.resize((RESIZE_TO[0], RESIZE_TO[1]), resample=Image.BOX)
image.save('image.png')
image.show()
