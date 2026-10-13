import streamlit as st
from vilib import Vilib

host = st.context.headers.get("host", "localhost").split(":")[0] #muss das?

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
    a.html(f'<img src="http://{host}:9000/mjpg" style="width:100%">')


