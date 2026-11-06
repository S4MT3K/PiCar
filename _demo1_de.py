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
        frame = camera.capture_array()
        success, frame = cv2.imencode('.jpg', frame)
        if not success:
            continue  
        frame = frame.tobytes()
        with lock:                 # das Schreiben ist jetzt im Lock
            lastFrame = frame
            if lastCallCameraPlay is not None and time.time() - lastCallCameraPlay > 10:
                cameraStop()
                print("Camera stopped due to inactivity.")
                break

def cameraPlay():
    global isFilming, lastFrame, lastCallCameraPlay, camera
    lastCallCameraPlay = time.time()
    camera = Picamera2()           # neue Kamera bei jedem Einschalten
    camera.configure(camera.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}))
    camera.start()
    isFilming = True
    threading.Thread(target=frameGenerator, daemon=True).start()   # Thread, damit nichts blockiert - ich bin nicht sicher, wie
    print ("camera up")                                            # er arbeitet, aber klar, er ist nötig

@acces.route("/stream")
def stream():
    return Response(toStream(), mimetype="multipart/x-mixed-replace; boundary=frame")   # toStream(), das ist der Generator
acces.run(host="0.0.0.0", port=8080, threaded=True)