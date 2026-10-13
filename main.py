

import streamlit as st

if st.button('Capture Image'):
    print('irgendwas')

if st.button('Shake Camera'):
    print('Shaking ass')

if st.button('Disconnect'):
    print('Disconnecting')

on = st.toggle("Camera on")

if on:
    st.write("Camera activated !")


