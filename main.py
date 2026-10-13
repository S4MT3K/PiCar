import streamlit as st
from vilib import Vilib

if st.button('Capture Image'):
    print('irgendwas')

if st.button('Shake Camera'):
    print('Shaking ass')

if st.button('Disconnect'):
    print('Disconnecting')

on = st.toggle("Camera on")

st.text("kameraFeed")
a = st.container(border= True)

if on:
    st.write("Camera activated !")
    Vilib.camera_start(vflip=False, hflip=False)


