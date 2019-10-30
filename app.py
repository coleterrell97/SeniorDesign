from flask import Flask, render_template, Response
from camera import CameraStream
import numpy as np
import cv2
import time, signal
app = Flask(__name__)

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
