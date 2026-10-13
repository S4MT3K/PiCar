import streamlit as st
from vilib import Vilib

# Kamera + Webstream nur EINMAL starten, nicht bei jedem Klick
@st.cache_resource
def kamera_starten():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=True)   # Stream auf http://<IP>:9000/mjpg
    return True

if st.button('Capture Image'):
    print('irgendwas')

if st.button('Shake Camera'):
    print('Shaking ass')

if st.button('Disconnect'):
    print('Disconnecting')

on = st.toggle("Camera on")

st.text("kameraFeed")
a = st.container(border=True)

if on:
    kamera_starten()
    st.write("Camera activated !")
    host = st.context.headers.get("host", "localhost").split(":")[0]
    a.html(f'<img src="http://{host}:8501/mjpg" style="width:100%">')