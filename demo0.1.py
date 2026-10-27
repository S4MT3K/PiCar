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

subscriber = 0
frames = None

def frame_generator():
    while subscriber != 0:
        frame = camera.capture_array()
        ok, frame = cv2.imencode(".jpg", frame)
        yield ok, frame

def get_or_start_generator():
    global subscriber, frames

    # allready filming
    if subscriber != 0 and frames:
        return frames

    # start new generator
    subscriber += 1
    frames = frame_generator()

    return frames

# ------------------------------------------------------------------------------
# routes
# ------------------------------------------------------------------------------

def camera_stream():
    global subscriber

    _frames = get_or_start_generator()

    try:
        while True:
            ok, frame = next(_frames)
            if not ok:
                continue
            frame = frame.tobytes()
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"
    finally:
        subscriber -= 1

@acces.route("/stream")
def stream():
    return Response(camera_stream(), mimetype="multipart/x-mixed-replace; boundary=frame")

# ------------------------------------------------------------------------------
# start web server
# ------------------------------------------------------------------------------

acces.run(host="0.0.0.0", port=8080, threaded=True)
