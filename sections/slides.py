"""Slide viewer — browse all four lecture decks as images."""
from pathlib import Path
import streamlit as st

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "slides"

DECKS = {
    "Lecture 1 — Accounting Basics for Valuation": "lecture1",
    "Lecture 2 — From Drivers to a 5-Year FCFF Forecast": "lecture2",
    "Lecture 3 — WACC, Terminal Value & the DCF": "lecture3",
    "Lecture 4 — Multiples, Precedents & Triangulation": "lecture4",
}


def _slides_for(folder):
    d = ASSETS / folder
    if not d.exists():
        return []
    return sorted(d.glob("slide-*.jpg"))


def render():
    st.title("Lecture slides")
    st.caption("The four session decks, browsable in-app. Use these alongside the practice "
               "questions — each question notes the slide it maps to.")

    deck_label = st.selectbox("Deck", list(DECKS.keys()))
    folder = DECKS[deck_label]
    slides = _slides_for(folder)
    if not slides:
        st.warning("Slide images not found for this deck. Re-run the build step that "
                   "renders PPTX → images into assets/slides/.")
        return

    key = f"slidepos_{folder}"
    st.session_state.setdefault(key, 0)
    pos = st.session_state[key] % len(slides)

    st.slider("Slide", 1, len(slides), pos + 1, key=f"sld_{folder}",
              on_change=lambda: st.session_state.__setitem__(
                  key, st.session_state[f"sld_{folder}"] - 1))
    pos = st.session_state[key] % len(slides)

    st.image(str(slides[pos]), width="stretch")

    c1, c2, c3 = st.columns([1, 2, 1])
    if c1.button("◀ Prev", width="stretch"):
        st.session_state[key] = (pos - 1) % len(slides)
        st.rerun()
    c2.markdown(f"<div style='text-align:center;color:#888'>Slide {pos + 1} of "
                f"{len(slides)}</div>", unsafe_allow_html=True)
    if c3.button("Next ▶", width="stretch"):
        st.session_state[key] = (pos + 1) % len(slides)
        st.rerun()
