import streamlit as st
import os
from PIL import Image


# Configure Streamlit page and state
st.set_page_config(page_title="Stay Positive", page_icon="🤗")


cols = st.columns([1, 3, 1])
with cols[1]:
    st.title("Stay Positive 🤗")
    st.markdown("Increase your happiness, day after day")
st.balloons()

st.image(Image.open(os.path.join("Images", "bench.jpg")))
