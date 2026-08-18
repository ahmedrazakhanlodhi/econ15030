"""Landing page."""
import streamlit as st

from data.questions import QUESTIONS, TOPICS


def render():
    st.title("ECON 15030 — Interview Prep")
    st.markdown("#### Basics of Corporate, Banking & Investment Finance · TA sessions")
    st.caption("Ahmed Raza Khan Lodhi · University of Chicago · September Term")

    st.markdown(
        "A single place to **practise the interview questions, run the models live, and "
        "review the slides** from the five TA sessions — from the three statements through "
        "a full DCF, multiples, and the Thoughtworks deal.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Practice questions", len(QUESTIONS))
    c2.metric("Live calculators", 7)
    c3.metric("Lecture decks", 4)
    c4.metric("Topics", len(TOPICS))

    st.divider()
    a, b = st.columns(2)
    with a:
        st.subheader("Start here")
        st.markdown(
            "- **Practice questions** — Study, Quiz, and Flashcard modes; numeric answers "
            "are graded automatically.\n"
            "- **Calculators** — FCFF, WACC/beta, a full DCF with live sensitivity, "
            "multiples, and the bidding ceiling.\n"
            "- **Lecture slides** — all four decks.\n"
            "- **Capstone** — the Thoughtworks take-private, interactive.")
    with b:
        st.subheader("Why the numbers always agree")
        st.markdown(
            "Every calculator calls one shared finance engine, so there's a single "
            "definition of FCFF (the unlevered NOPAT route), one DCF assembly, and a "
            "sensitivity table that recomputes terminal FCFF for each growth case. The "
            "practice bank's numeric answers are validated against that same engine, so "
            "the calculators and the answer keys stay in agreement.")

    st.info("Pick a section from the sidebar to begin.")
