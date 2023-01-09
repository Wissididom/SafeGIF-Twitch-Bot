import imageio.v3 as iio
import numpy
import cv2

# Defines the minimum amount of average luminosity change to the previous frame
# for a frame to be considered a flash.
FLASH_THRESHOLD = 50

# The minimum amount of flashing frames for a gif to be rejected.
# This is a percentage, so 0.25 means at least 25% of frames must be flashes for
# the gif to be rejected.
FLASHING_FRAME_COUNT_THRESHOLD = 0.25


def process_gif(gif_path):
    def get_luminance_diff(luminance_frame, luminance_prev_frame):
        bgr = cv2.cvtColor(luminance_frame, cv2.COLOR_RGB2BGR)
        luminances = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

        prev_bgr = cv2.cvtColor(luminance_prev_frame, cv2.COLOR_RGB2BGR)
        prev_luminances = cv2.cvtColor(prev_bgr, cv2.COLOR_BGR2GRAY)

        diff = cv2.subtract(luminances, prev_luminances)
        return numpy.average(diff)

    gif = iio.imread(gif_path)
    total_frames = len(gif)

    num_flashes = 0
    prev_frame = None
    for i, frame in enumerate(gif):
        if i == 0:
            prev_frame = frame
            continue

        luminance_diff = get_luminance_diff(frame, prev_frame)

        if luminance_diff >= FLASH_THRESHOLD:
            num_flashes += 1

        prev_frame = frame

    return num_flashes >= FLASHING_FRAME_COUNT_THRESHOLD * total_frames
