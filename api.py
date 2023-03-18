import cv2
import imageio.v3 as iio
import numpy
import requests
import urllib.parse
from io import BytesIO
from PIL import Image

# These values are not backed by resources just random guesses (trial and error)

# Defines the minimum amount of average luminosity change to the previous frame
# for a frame to be considered a flash.
FLASH_THRESHOLD = 25

# The maximum amount of flashing frames per second for a gif not to be rejected.
# For example a gif with a looping duration of 500ms and 2 flashes will result in
# a value of 4 flashes per second.
MAX_FLASHES_PER_SECOND = 1.5


def is_url(string):
    # Parse the string as a URL
    parsed = urllib.parse.urlparse(string)

    # Check if the scheme is present
    return bool(parsed.scheme)


def get_luminance_diff(luminance_frame, luminance_prev_frame):
    bgr = cv2.cvtColor(luminance_frame, cv2.COLOR_RGB2BGR)
    luminances = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

    prev_bgr = cv2.cvtColor(luminance_prev_frame, cv2.COLOR_RGB2BGR)
    prev_luminances = cv2.cvtColor(prev_bgr, cv2.COLOR_BGR2GRAY)

    diff = cv2.subtract(luminances, prev_luminances)
    iio.imwrite("debug.jpg", diff)
    return diff


def get_duration(img):
    img.seek(0)
    duration = 0
    while True:
        try:
            duration += img.info['duration']
            img.seek(img.tell() + 1)
        except EOFError:
            return duration


def process_gif(gif_path):
    gif = iio.imread(gif_path)

    total_frames = len(gif)
    if total_frames < 2:
        return False

    if is_url(gif_path):
        response = requests.get(gif_path)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(gif_path)

    loop_duration = get_duration(img)

    num_flashes = 0
    prev_frame = None
    for i, frame in enumerate(gif):
        if i == 0:
            prev_frame = frame
            continue

        luminance_diff = get_luminance_diff(frame, prev_frame)
        average_diff = numpy.average(luminance_diff)

        if average_diff >= FLASH_THRESHOLD:
            num_flashes += 1

        prev_frame = frame

    img.close()

    return num_flashes * (1000 / loop_duration) >= MAX_FLASHES_PER_SECOND
