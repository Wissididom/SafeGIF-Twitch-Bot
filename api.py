import cv2
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
    return diff


def process_gif(gif_path):
    if is_url(gif_path):
        response = requests.get(gif_path)
        img = Image.open(BytesIO(response.content))
    else:
        img = Image.open(gif_path)

    if not img.is_animated:
        print("Image is not animated.")
        return False

    duration = 0
    num_flashes = 0
    prev_frame = None
    for i in range(0, img.n_frames):
        img.seek(i)
        duration += img.info['duration']
        frame = numpy.array(img.convert('RGB'))

        # If not the first frame calculate diff to previous frame
        # If too much average diff in luminance the frame transition is considered a flash
        if i != 0:
            luminance_diff = get_luminance_diff(frame, prev_frame)
            average_diff = numpy.average(luminance_diff)

            if average_diff >= FLASH_THRESHOLD:
                num_flashes += 1

        prev_frame = frame

    img.close()

    return num_flashes * (1000 / duration) >= MAX_FLASHES_PER_SECOND
