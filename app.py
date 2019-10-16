from flask import Flask, render_template, Response
from camera import CameraStream
import numpy as np
import cv2
import time
app = Flask(__name__)

# Get camera sources
two_cameras = input('Do you have two cameras (Y/N)? ').lower() == 'y'
src1 = int(input('Camera source 1: '))
if two_cameras: src2 = int(input('Camera source 2: '))

global cap1, cap2
# Start video capturing
cap1 = CameraStream(src=src1).start()
if two_cameras: cap2 = CameraStream(src=src2).start()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen_frame():
    """Video streaming generator function."""
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
            convert = cv2.imencode('.jpg', cap1.frame)[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # Concate frame one by one and show result

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#background process happening without any refreshing
@app.route('/flip_cameras')
def flip_cameras():
    print("got here")
    global cap1, cap2
    if two_cameras:
        temp = cap1
        cap1 = cap2
        cap2 = temp
        print("flipped cameras")
    return("")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, threaded=True)
