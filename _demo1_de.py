from flask import Flask, Response
from picamera2 import Picamera2
import cv2, time, threading

acces = Flask(__name__)
FPS = 30

isFilming = False
lastFrame = None
frameToStream = None
lastCallCameraPlay = None
camera = None                      # wird in cameraPlay() erstellt, nicht am Anfang
lock = threading.Lock()

def cameraStop():
    global isFilming, lastFrame
    isFilming = False
    camera.stop()  # das geht, weil camera in cameraPlay() = Picamera2() ist
    camera.close()
    lastFrame = None
    print ("camera down")

def toStream(): ### Hier ist der Generator. Die Route ruft ihn auf, und er ruft intermediateFrame() auf, um das Frame zu holen
    global lastFrame, frameToStream # Hier ist das yield, das das Frame an den Browser schickt, und es ruft intermediateFrame() auf, um das Frame zu holen
    if not isFilming:              # wenn die Kamera aus ist, schalten wir sie ein
        cameraPlay()
    interval = 1 / FPS
    tick = time.time()
    while True:                    # Schleife, um ohne Pause Frames zu schicken
        intermediateFrame()        # holt das Frame von der Übergabe
        if frameToStream is not None:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frameToStream + b'\r\n')
        tick += interval
        delay = tick - time.time()
        if delay > 0:
            time.sleep(delay)
        else:
            tick = time.time()

def intermediateFrame():
    global lastFrame, frameToStream, lastCallCameraPlay
    with lock:
        frameToStream = lastFrame
        lastCallCameraPlay = time.time()   # trägt die Abholung ein (für den Timeout)
    # ohne while und ohne toStream() aufzurufen: gibt nur das Frame weiter

def frameGenerator():
    global lastFrame, frameToStream, isFilming, lastCallCameraPlay
    while isFilming:
        frame =