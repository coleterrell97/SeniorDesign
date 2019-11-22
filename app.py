from flask import Flask, render_template, Response, request, jsonify
from camera import CameraStream
import numpy as np
import cv2
import time, signal
import json
import re
app = Flask(__name__)

config_settings = {
                    "brightness" : 15,
                    "contrast" : 15,
                    "saturation" : 32,
                    "sharpness" : 16,
                    "gamma" : 220,
                    "white" : 5000,
                    "gain" : 0,
                    "pan" : 0,
                    "tilt" : 0,
                    "zoom" : 100,
                    "exposure" : 312,
                    "backlight" : 0,
                    "roll" : 0,
                    "iris" : 0,
                    "focus" : 0,
                    "hue" : 0
                    }

# Get camera sources
two_cameras = input('Do you have two cameras (Y/N)? ').lower() == 'y'
src1 = int(input('Camera source 1: '))
if two_cameras:	src2 = int(input('Camera source 2: '))

global cap1, cap2
# Start video capturing
cap1 = CameraStream(src=src1, resize=(500,500)).start()
if two_cameras: cap2 = CameraStream(src=src2).start()

# Video streaming home page
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/update_values", methods=["POST"])
def update_values():
    props = ['brightness', 'contrast', 'saturation', 'sharpness', 'gamma', 'white', 'gain', 'pan', 'tilt', 'zoom', 'exposure', 'backlight', 'roll', 'iris', 'focus', 'hue']

    for prop in props:
        config_settings[prop] = int(request.form.get(prop))

    file_to_open = "./config.json"
    with open(file_to_open, "w") as f:
        f.write(json.dumps(config_settings))

    print(config_settings)
    return render_template('index.html')


@app.route("/send_values", methods=["GET"])
def send_values():
    return jsonify(config_settings)


@app.route('/settings')
def settings():
    return render_template('settings.html')


# Generates the images for the video stream
def gen_frame():
    if two_cameras: # Stitch two feeds together
        while cap1 and cap2:
            frame1 = cap1.frame
            frame2 = cap2.frame
            joined = np.concatenate((frame1, frame2), axis=1)
            convert = cv2.imencode('.jpg', joined)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # Concate frame one by one and show result
    else: # Only one camera feed
        while cap1:
            # convert = cv2.imencode('.jpg', cap1.frame)[1].tobytes()
            bytes = cap1.read()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + bytes + b'\r\n') # Concate frame one by one and show result

# Video streaming route. Put this in the src attribute of an img tag
@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Ends the video feed processes -- joins all threads
def exit(sigal_num, signal_frame):
    cap1.stop()
    if two_cameras: cap2.stop()
    print() # Makes the path appear in the right spot afterwards

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
    signal.signal(signal.SIGINT, exit) # Calls exit function on ctrl^c
