from flask import Flask, Response
from picamera2 import Picamera2 # type: ignore *** Windows issue ***
import cv2, time

# ------------------------------------------------------------------------------
# setup
# ------------------------------------------------------------------------------

acces = Flask(__name__)    #We make a flask instance so we can use it later
FPS = 30   #set a system speed

camera = Picamera2()
camera.configure(camera.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}))
camera.start() # Resources?

# ------------------------------------------------------------------------------
# frame generator
# ------------------------------------------------------------------------------

def frame_generator():
    while True:
        frame = camera.capture_array()
        ok, frame = cv2.imencode(".jpg", frame)
        if not ok:
            continue
        yield frame

# ------------------------------------------------------------------------------
# routes
# ------------------------------------------------------------------------------

def camera_stream():
    frames = frame_generator()

    while True:
        frame = next(frames).tobytes()
        yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"

@acces.route("/stream")
def stream():
    return Response(camera_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")

# ------------------------------------------------------------------------------
# start web server
# ------------------------------------------------------------------------------

acces.run(host="0.0.0.0", port=8080, threaded=True)
