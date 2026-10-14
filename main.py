
import streamlit as st
from vilib import Vilib
from picamera2 import Picamera2
import time
import numpy as np #nur für grau screen

#------------------------------------------------------------------------------
### GUI
#------------------------------------------------------------------------------



st.set_page_config(page_title="PiCar Camera-Interface")
st.title("PiCar Camera-Interface")
 
bild, tasten = st.columns([2, 1], vertical_alignment="center")
on = st.toggle("Camera On/Off", value=False, key="camera_toggle")
platz = st.empty()
 
 
def zeige(text):
    platz.info(text)
    time.sleep(3)
    platz.empty()
 
 
 
with bild:
    grau = np.full((360, 480, 3), 150, dtype=np.uint8)
    st.image(grau, width="stretch")



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
        Vilib.picam2 = Picamera2();

    def toggle(self):
        if self.__state:
            self.off()
        else:
            self.on()

@st.cache_resource
def get_camera():
    return Camera()
camera = get_camera()

on = st.toggle(
    "Camera on",
    key="camera_on",
    value=camera.state,
    persist_state="page",
)

if on:
    camera.on()
else:
    camera.off()

st.text("kameraFeed")
container = st.container(border=True)

if camera.state:
    st.write("Camera activated !")
    host = st.context.headers.get("host").split(":")[0]
    container.image(f"http://{host}:9000/mjpg")

# ------------------------------------------------------------------------------
# buttons
# ------------------------------------------------------------------------------
 
with bild:
    grau = np.full((360, 480, 3), 150, dtype=np.uint8)
    st.image(grau, width="stretch")
 
with tasten:
    if st.button("Take Screenshot", width="stretch"):
        zeige("Take Screenshot gedrückt")
    if st.button("Shake Camera", width="stretch"):
        zeige("Shake Camera gedrückt")
    if st.button("Disconnect", width="stretch"):
        zeige("Disconnect gedrückt")
    if on:
        zeige("Camera ON")


