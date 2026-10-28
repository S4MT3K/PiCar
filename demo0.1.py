from flask import Flask, Response
from picamera2 import Picamera2 # type: ignore *** Windows issue ***
import cv2, time

# ------------------------------------------------------------------------------
# setup
# ------------------------------------------------------------------------------

# We make a flask instance so we can use it later
acces = Flask(__name__)    

# set a system speed
FPS = 30

camera = Picamera2()
camera.configure(camera.create_video_configuration(main={
    "size": (640, 480),
    "format": "RGB888",
}))

# Resources?
camera.start()

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
    return Response(
        camera_stream(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )

# ------------------------------------------------------------------------------
# start web server
# ------------------------------------------------------------------------------

acces.run(host="0.0.0.0", port=8080, threaded=True)
