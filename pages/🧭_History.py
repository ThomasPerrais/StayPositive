import streamlit as st
from datetime import date, timedelta

from databases.es_connector import exist_for_date, get_for_date
from nlp.chatgpt_summary import summarize_week
from variables import DAYS, SUMMARY_TYPES, MIN_MOMENTS_SUMMARY, SIZE, DEFAULT_LANG


# Variables & session_state variables

week_moments = 0
current = date.today().weekday()

if not "moments" in st.session_state:
    st.session_state.moments = [] if not exist_for_date() else get_for_date()   
if not "weekgap" in st.session_state:
    st.session_state.weekgap = 0
if not "chatgpt_summary" in st.session_state:
    st.session_state.chatgpt_summary = ""
if not "error" in st.session_state:
    st.session_state.error = ""
if not "summary_type" in st.session_state:
    st.session_state.summary_type = SUMMARY_TYPES[DEFAULT_LANG][0]

def get_moments(gap: int):
    st.session_state.moments = []
    try:
        st.session_state.moments = get_for_date(gap)
    except:
        st.error("Error while retrieving moments, try again later...")


def change_week(prev: bool):
    st.session_state.moments = []  # clear moments
    st.session_state.chatgpt_summary = ""  # clear chatGPT summary
    if prev:
        st.session_state.weekgap += 1
    else:
        st.session_state.weekgap -= 1


def chatgpt_summary(summary_type: str):
    with placeholder:
        with st.spinner("⏳ - Waiting for ChatGPT computation..."):
            week_moments = []
            for i in range(SIZE):
                gap = i - current - st.session_state.weekgap * SIZE
                week_moments.append(get_for_date(gap) if gap <= 0 else [])
            summary = summarize_week(week_moments, summary_type)
            if summary.startswith("[ERROR]"):
                st.session_state.error = "Error when calling ChatGPT, try again in a moment..."
            else:
                st.session_state.chatgpt_summary = summary


# upper part: navigate between weeks
navigate = st.columns([1, 5, 1])
with navigate[0]:
    st.button(label="<< prev", on_click=change_week, args=(True,))
with navigate[2]:
    st.button(label="next >>", on_click=change_week, args=(False,), disabled=st.session_state.weekgap == 0)    


cols = st.columns(SIZE)
for i in range(len(cols)):
    with cols[i]:
        gap = i - current - st.session_state.weekgap * SIZE
        exist = exist_for_date(gap)
        if exist:
            week_moments += 1
        date = date.today() - timedelta(days=-gap)
        st.write(DAYS[DEFAULT_LANG][i])
        st.button(label="{}/{}".format(date.day, date.month),
                  on_click=get_moments,
                  args = (gap,),
                  type = "primary" if gap == 0 else "secondary",
                  disabled=not exist)


st.markdown("""---""")
if st.session_state.moments:
    cols = st.columns(3)
    for i, moment in enumerate(st.session_state.moments):
        with cols[i]:
            st.text_area(label = "Moment {}".format(str(i + 1)), value=moment)


st.markdown("""---""")
cols = st.columns(2)
with cols[1]:
    st.session_state.summary_type = st.selectbox(label="type of summary",
                                                 options=SUMMARY_TYPES[DEFAULT_LANG],
                                                 label_visibility="collapsed")
with cols[0]:
    st.button(label="Week Summary by ChatGPT",
              on_click=chatgpt_summary,
              args = (st.session_state.summary_type,),
              disabled=week_moments < MIN_MOMENTS_SUMMARY)


if st.session_state.chatgpt_summary:
    st.text_area(label="Summary", value=st.session_state.chatgpt_summary, height=200)

placeholder = st.empty()  # placeholder is at the end of the page and is used to display waiting spinner of ChatGPT
