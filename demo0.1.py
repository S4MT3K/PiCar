from flask import Flask, Response
from picamera2 import Picamera2 # type: ignore *** Windows issue ***
import cv2, time

acces = Flask(__name__)    #We make a flask instance so we can use it later
FPS = 30                   #set a system speed
isOn = False
user = 0
camera = None

def startCamera():
    global camera, isOn
    if not isOn:
        camera = Picamera2()  # initiation of the camera
        camera.configure(camera.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}))  # setting the parameters for it based on the camera type
        camera.start()  # starting the hardware
        print("camera up")  # A simple print to console as visual feedback
        isOn = True

def camerastream():                                                                                            #Our producer and consumer in one, grabbing and sending the frame both happen here
        global isOn, user, camera
        startCamera()
        user += 1
        interval = 1 / FPS                                                                                     #setting how long the program has to cycle
        tick = time.time()  #NOW                                                                               #starting to track the cycle duration
        try :                                                                                                  #we wrap the loop so the camera is shut down however it ends
            while True :                                                                                       #here begins the actual loop and runs as long as the browser is watching
                frame = camera.capture_array()                                                                 #we grab the frame provided by the hardware
                ok, frame = cv2.imencode(".jpg", frame)                                                        #check if there is a frame and use Cv2 to render the frame into a JPG
                if not ok:                                                                                     #if the frame was not valid we can skipp the rest
                    continue
                frame = frame.tobytes()                                                                        #otherwise we format it
                yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + frame + b"\r\n"                         #and send it out right away after wrapping it html passable
                tick += interval                                                                               #our cycle control sets the time the next cycle should start
                delay = tick - time.time()                                                                     #we check if we were faster or needed more time
                if delay > 0:                                                                                  #if there is still time we wait till the next cycle should start
                    time.sleep(delay)
                else:                                                                                          #or we start immediately and set a new default time for the next cycle
                    tick = time.time()
        finally :                                                                                              #when the browser leaves, flask closes our function and we land here
            user -= 1
            if not user:
                camera.stop()                                                                                      #so we tell the hardware to first stop
                camera.close()                                                                                     #and then shut down to save resources
                print ("camera down")
                isOn = False#together with a simple console feedback

@acces.route("/stream")                                                                     #acces gets defined via a key
def stream():                                                                               #and a function defined corresponding to the key
    return Response(camerastream(), mimetype="multipart/x-mixed-replace; boundary=frame")   #in our case beginning to send frames

acces.run(host="0.0.0.0", port=8080, threaded=True)     #last we start the flask, telling here where to listen for requests