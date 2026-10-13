import time
import numpy as np
import streamlit as st
from vilib import Vilib


def bild_da():
    return isinstance(Vilib.img, np.ndarray)


@st.cache_resource
def kamera_starten():
    Vilib.camera_start(vflip=False, hflip=False)
    Vilib.display(local=False, web=False)
    for _ in range(50):            # max. 5 s auf das erste Bild warten
        if bild_da():
            break
        time.sleep(0.1)
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


@st.fragment(run_every=0.1)
def kamera_feed():
    if bild_da():
        st.image(Vilib.img, channels="BGR")
    else:
        st.caption("Warte auf Kamerabild …")


if on:
    kamera_starten()
    st.write("Camera activated !")
    with a:
        kamera_feed()