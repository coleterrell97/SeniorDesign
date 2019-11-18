import cv2
from camera import CameraStream
import numpy as np
import signal, sys, json

WINDOW_TITLE = 'Video Stream'
CONFIG_FILE = 'config.json'
WIDTH = 1440 # Screen width
HEIGHT = 900 # Screen height
MAX_FRAMERATE = 30 # Frames per second
CURRENT_CONFIG = None # Current OpenCV camera settings

# CV2 enumerator to be used for adjusting properties
PROPERTIES = [
    (cv2.CAP_PROP_BRIGHTNESS, 'CAP_PROP_BRIGHTNESS'),
    (cv2.CAP_PROP_CONTRAST, 'CAP_PROP_CONTRAST'),
    (cv2.CAP_PROP_SATURATION, 'CAP_PROP_SATURATION'),
    (cv2.CAP_PROP_SHARPNESS, 'CAP_PROP_SHARPNESS'),
    (cv2.CAP_PROP_GAMMA, 'CAP_PROP_GAMMA'),
    (cv2.CAP_PROP_WHITE_BALANCE_BLUE_U, 'CAP_PROP_WHITE_BALANCE_BLUE_U'),
    (cv2.CAP_PROP_GAIN, 'CAP_PROP_GAIN'),
    (cv2.CAP_PROP_PAN, 'CAP_PROP_PAN'),
    (cv2.CAP_PROP_TILT, 'CAP_PROP_TILT'),
    (cv2.CAP_PROP_ZOOM, 'CAP_PROP_ZOOM'),
    (cv2.CAP_PROP_EXPOSURE, 'CAP_PROP_EXPOSURE'),
    (cv2.CAP_PROP_BACKLIGHT, 'CAP_PROP_BACKLIGHT'),
    (cv2.CAP_PROP_ROLL, 'CAP_PROP_ROLL'),
    (cv2.CAP_PROP_IRIS, 'CAP_PROP_IRIS'),
    (cv2.CAP_PROP_FOCUS, 'CAP_PROP_FOCUS'),
    (cv2.CAP_PROP_HUE, 'CAP_PROP_HUE'),
]

# Crops each image to the proper viewing size based on the WIDTH and HEIGHT
# variables. This makes it so that the feed will take up the entire screen.
# The main goal is to fit the proper aspect ratio. Returns the cropped image.
def crop(img):
    # Get the deminsion variables.
    # We want the desired width to be the screen width divided by two
    # since there are two images next to each other horizontally
    height, width, channels = img.shape
    desired_width = WIDTH // 2
    desired_height = HEIGHT
    centerX = width // 2
    centerY = height // 2

    # Calculate the crop in the scenario where the desired display size is actually
    # larger than the camera images
    if desired_width > width or desired_height > height:
        desired_aspect = desired_width / desired_height
        width_difference = desired_width - width
        height_difference = desired_height - height

        # Determine the optimal way to get the proper aspect ratio
        if height_difference > 0 and width_difference > 0:
            if height_difference > width_difference:
                new_width = int(desired_aspect * height)
                minX, maxX = centerX - (new_width//2), centerX + (new_width//2)
                img = img[:, minX:maxX]
            else:
                new_height = int(width / desired_aspect)
                minY, maxY = centerY - (new_height//2), centerY + (new_height//2)
                img = img[minY:maxY, :]
        elif height_difference > 0:
            new_width = int(desired_aspect * height)
            minX, maxX = centerX - (new_width//2), centerX + (new_width//2)
            img = img[:, minX:maxX]
        else:
            new_height = int(width / desired_aspect)
            minY, maxY = centerY - (new_height//2), centerY + (new_height//2)
            img = img[minY:maxY, :]

        return cv2.resize(img, (desired_width, desired_height))

    # *** This code has not been confirmed to work ***
    # Calculate and preform the crop in the scenario where the images are larger
    # than the desired display size
    minX, maxX = centerX - (desired_width//2), centerX + (desired_width // 2)
    minY,maxY = centerY - (desired_height//2), centerY + (desired_height // 2)
    return img[minX:maxX, minY:maxY]

# Ends the video feed processes -- joins all threads
def exit(sigal_num=None, signal_frame=None):
    stream1.stop()
    stream2.stop()
    cv2.destroyAllWindows()
    print('\nGoodbye')
    sys.exit()

# Get camera sources and begin the streams
src1 = int(input('Camera source 1: '))
src2 = int(input('Camera source 2: '))
stream1 = CameraStream(src=src1).start()
stream2 = CameraStream(src=src2).start()

# Initialize other imporant parts
signal.signal(signal.SIGINT, exit) # Calls exit function on ctrl^c
cv2.namedWindow(WINDOW_TITLE, cv2.WINDOW_NORMAL)
zoom_amount = 1

# Streaming loop: continually get camera feeds and display them to the screen
while 1:
    # Read the camera configurations
    with open(CONFIG_FILE) as f:
        data = json.load(f)

    # Apply the loaded configurations. Only update the settings when the config
    # file is changed
    if data != CURRENT_CONFIG:
        CURRENT_CONFIG = data
        for property, property_str in PROPERTIES:
            property_value = float(CURRENT_CONFIG[property_str])
            stream1.stream.set(property, property_value)
            stream2.stream.set(property, property_value)

    # Get the images and crop them to the proper viewing size
    left = stream1.read()
    right = stream2.read()
    left = crop(left)
    right = crop(right)

    # Stitch together the final image and show it
    dual = np.concatenate((left, right), axis=1)
    cv2.imshow(WINDOW_TITLE, dual)
    cv2.waitKey(1000//MAX_FRAMERATE)
