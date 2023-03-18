import cv2
import imageio.v3 as iio
import numpy
import api as safegif
import matplotlib.pyplot as plt
import requests
from PIL import Image
from io import BytesIO

FLASH_THRESHOLD = 25

gif_path = "https://static-cdn.jtvnw.net/emoticons/v2/emotesv2_502bf8fd256b44348d9a5b9c546bee67/default/dark/3.0"
gif = iio.imread(gif_path)
total_frames = len(gif)

if safegif.is_url(gif_path):
    response = requests.get(gif_path)
    img = Image.open(BytesIO(response.content))
else:
    img = Image.open(gif_path)

loop_duration = safegif.get_duration(img)
print(str(loop_duration) + "ms")

luminance_diffs = []
average_diffs = []

num_flashes = 0
prev_frame = None
for i, frame in enumerate(gif):
    if i == 0:
        prev_frame = frame
        continue

    luminance_diff = safegif.get_luminance_diff(frame, prev_frame)
    average_diff = numpy.average(luminance_diff)

    luminance_diffs.append(luminance_diff)
    average_diffs.append(average_diff)

    if average_diff >= FLASH_THRESHOLD:
        num_flashes += 1

    prev_frame = frame

print(str(num_flashes) + " Flashes")

iio.imwrite("debug.gif", luminance_diffs, format='gif', duration=500)
plt.plot(average_diffs)
plt.xlabel('Frame')
plt.ylabel('Avg. luminosity diff')
plt.savefig('debug.png')
