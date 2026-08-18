"""
ECON 15030 Interview Prep — Streamlit app.

Run locally:   streamlit run app.py
Deploy:        push to GitHub, then create an app on share.streamlit.io
               pointing at this repo's app.py (see README).
"""
import streamlit as st

st.set_page_config(
    page_title="ECON 15030 · Interview Prep",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

from sections import home, practice, calculators, slides, case  # noqa: E402

PAGES = {
    "": [st.Page(home.render, title="Overview", icon="🏠",
                 url_path="overview", default=True)],
    "Prepare": [
        st.Page(practice.render, title="Practice questions", icon="✍️",
                url_path="practice"),
        st.Page(calculators.render, title="Calculators", icon="🧮",
                url_path="calculators"),
    ],
    "Reference": [
        st.Page(slides.render, title="Lecture slides", icon="🖼️",
                url_path="slides"),
        st.Page(case.render, title="Thoughtworks capstone", icon="📉",
                url_path="capstone"),
    ],
}

with st.sidebar:
    st.markdown("### ECON 15030")
    st.caption("Corporate, Banking & Investment Finance")

nav = st.navigation(PAGES)
nav.run()

with st.sidebar:
    st.divider()
    st.caption("TA sessions · Ahmed Raza Khan Lodhi\n\nUniversity of Chicago")
