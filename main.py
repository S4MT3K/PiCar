import streamlit as st
from vilib import Vilib
from picamera2 import Picamera2
import time
import numpy as np  # nur für grau screen

st.set_page_config(page_title="PiCar Camera-Interface")


# ------------------------------------------------------------------------------
# video
# ------------------------------------------------------------------------------

class Camera:
    __state: bool

    def __init__(self):
        self.__state = False

    @property
    def state(self):
        return self.__state

    def on(self):
        if self.__state:
            return

        self.__state = True
        Vilib.camera_start()

        # we only need the web view
        Vilib.display(local=False, web=True)

    def off(self):
        if not self.__state:
            return

        self.__state = False
        Vilib.camera_close()

        # closing the camera will distroy the picamera2 object configurations
        # the configurations are only created on __init__ so simply create a new instance
        Vilib.picam2 = Picamera2()

    def toggle(self):
        if self.__state:
            self.off()
        else:
            self.on()


@st.cache_resource
def get_camera():
    return Camera()


camera = get_camera()


# ------------------------------------------------------------------------------
# GUI
# ------------------------------------------------------------------------------

st.title("PiCar Camera-Interface")

bild, tasten = st.columns([2, 1], vertical_alignment="center")

with bild:
    bildplatz = st.empty()

with tasten:
    screenshot = st.button("Take Screenshot", width="stretch")
    shake = st.button("Shake Camera", width="stretch")
    disconnect = st.button("Disconnect", width="stretch")

on = st.toggle("Camera On/Off", value=camera.state, key="camera_toggle")
platz = st.empty()


def zeige(text):
    platz.info(text)
    time.sleep(3)
    platz.empty()


if on:
    camera.on()
    host = st.context.headers.get("host").split(":")[0]
    bildplatz.image(f"http://{host}:9000/mjpg", width="stretch")
else:
    camera.off()
    grau = np.full((360, 480, 3), 150, dtype=np.uint8)
    bildplatz.image(grau, width="stretch")

if screenshot:
    zeige("Take Screenshot gedrückt")
if shake:
    zeige("Shake Camera gedrückt")
if disconnect:
    zeige("Disconnect gedrückt")