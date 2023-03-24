"""Streamlit app to store 3 happy moments everyday"""

# Import from standard library
import logging
from typing import List
from datetime import date, timedelta

# Import from 3rd party libraries
import streamlit as st

# Import from other files
from databases.es_connector import store, exist_for_date
from variables import DAYS, TODAY, AUTHORIZED_LATE_DAYS, NUM_MOMENTS, DEFAULT_LANG

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Configure Streamlit page and state
st.set_page_config(page_title="Stay Positive", page_icon="🤗")


# session_state variables
if "error" not in st.session_state:
    st.session_state.error = ""

def _day(gap: int):
    if gap == 0:
        return TODAY[DEFAULT_LANG]
    return DAYS[DEFAULT_LANG][(date.today() - timedelta(days = gap)).weekday()]

days_opts = { _day(i) : i for i in range(AUTHORIZED_LATE_DAYS + 1) }

cols = st.columns(2)
with cols[0]:
    st.markdown("Can you think of the three moments that enlightened your day?")
with cols[1]:
    gap = st.selectbox(label="Store moments for: ", options=days_opts.keys())

st.markdown("---")

moments = [st.text_input(label="Moment {}".format(str(i+1))) for i in range(NUM_MOMENTS)]


def store_moments(gap: int, moments: List[str]):
    moments = [m for m in moments if m]
    if not len(moments):
        st.session_state.error = "Write at least one moment before storing"
        return
    
    st.session_state.error = ""
    if exist_for_date(-gap):
        st.session_state.error = "Moments already stored for that day"
        return
    
    with st.spinner('Storing moments...'):
        res = store(moments=moments, gap=gap)
    if res:
        st.balloons()
        st.success('Moments stored!', icon="✅")
    else:
        st.session_state.error = "Error when saving moments, try again later..."


st.button(
    label="Store",
    type="primary",
    on_click=store_moments,
    args=(days_opts[gap], moments),
)

if st.session_state.error:
    st.error(st.session_state.error)
