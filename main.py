import streamlit as st
from vilib import Vilib

@st.cache_resource
def kamera_starten():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=False)   # kein Fenster, kein Webserver nötig
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

@st.fragment(run_every=0.1)          # nur dieser Teil läuft alle 0,1 s neu
def kamera_feed():
    if Vilib.img is not None:
        st.image(Vilib.img, channels="BGR")

if on:
    kamera_starten()
    st.write("Camera activated !")
    with a:
        kamera_feed()