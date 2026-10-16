import time
import math 
from picarx import Picarx

px = Picarx()

def smooth_shake(duration=3.0, frequency=15, amplitude=8):
    start_time = time.time()
    
    while time.time() - start_time < duration:
        elapsed = time.time() - start_time

        angle = amplitude * math.sin(frequency * elapsed)

        px.set_cam_pan_angle(angle)

        time.sleep(0.01)

    px.set_cam_pan_angle(0)
    px.set_cam_tilt_angle(0)

if __name__ == "__main__":
    try: 
        print("Starte Kamera-Shake...")

        smooth_shake(2.0, 20, 6)

    except KeyboardInterrupt:
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        print("Programm beendet.")