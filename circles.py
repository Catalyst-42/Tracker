from math import pi, sin, cos

import numpy
from PIL import Image

import save
from setup import setup

from utils import h, d, w

ARGS, ACTIVITIES = setup("circles")
all_experiment_time = save.timestamp - save.activities[0][1]
experiment_start_time = save.activities[0][1]

start_radius = ARGS["START_RADIUS"]
image_side = (
    round((start_radius + all_experiment_time/w))*2 + 8
    if ARGS["IMAGE_SIDE"] == "auto" else
    ARGS["IMAGE_SIDE"]
)

# Create image canvas
image = numpy.zeros((image_side, image_side, 3), dtype=numpy.uint8)
image[:][:] = ARGS["COLOR_BG"]

# Form dots
for i, activity in enumerate(save.activities):
    activity_name, timestamp, *_ = activity
    if activity_name == ARGS["VOID"]: continue
    
    x = (timestamp + ARGS["UTC_OFFSET"]) % d / h

    if i != len(save.activities) - 1: 
        days = (timestamp - experiment_start_time) / d
    else: 
        days = (save.timestamp - experiment_start_time) / d

    y = round(cos(pi * x / 12)*(start_radius + days/7) - image_side/2)
    x = round(sin(pi * x / 12)*(start_radius + days/7) + image_side/2)
    
    # if activity == "Сон":
    image[x][y] = ACTIVITIES[activity_name]

image_side *= ARGS["IMAGE_SCALE"]

image = Image.fromarray(image)
image = image.transpose(Image.Transpose.ROTATE_90)
image = image.resize((image_side, image_side), resample=Image.Resampling.BOX)

if ARGS["IMAGE"]:
    image.save(f"circles.png")

if not ARGS["SILENT"]:
    image.show()
