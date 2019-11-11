from threading import Thread, Lock
import cv2

class CameraStream(object):
    def __init__(self, src=0, resize=None):
        self.stream = cv2.VideoCapture(src)
        self.resize = resize
        self.stream.set(3,1280)
        self.stream.set(4,720)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    # Begins the continual update() thread
    def start(self):
        if self.started:
            print("already started!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    # Threaded function that is coninually reading the camera stream
    # Also resizes the frame if necessary
    def update(self):
        while self.started:
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            if self.resize:
                self.grabbed, self.frame = grabbed, cv2.resize(frame, self.resize)
            else:
                self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    # Locks the thread to allow for frame reading
    # This is safer than pulling the CameraStream.frame variable
    def read(self):
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    # Makes the camera stream resize the captured frames to the specified dimensions
    def resize(width, height=None):
        if width == None: self.resize = None # Turns resizing off
        else: self.resize = (width, height)

    # Joins the child thread back to the parent to prevent a zombie thread
    def stop(self):
        self.started = False
        self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback):
        self.stream.release()
