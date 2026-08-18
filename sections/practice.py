"""Practice question engine: Study, Quiz, and Flashcard modes."""
import random
import streamlit as st

from data.questions import QUESTIONS, TOPICS, LEVELS, FORMATS, by_topic

TOPIC_ICON = {
    "Accounting": "📒", "FCFF & Drivers": "💵",
    "WACC & DCF": "📉", "Multiples & Deals": "🤝",
}
LEVEL_COLOR = {"Core": "#2E7D32", "Stretch": "#B8860B", "Interview-hard": "#800000"}


# ------------------------------------------------------------------ state
def _init_state():
    st.session_state.setdefault("answered", {})   # id -> bool correct
    st.session_state.setdefault("quiz_order", [])
    st.session_state.setdefault("quiz_pos", 0)
    st.session_state.setdefault("flash_pos", 0)
    st.session_state.setdefault("flash_show", False)


def _badge(text, color):
    return (f"<span style='background:{color};color:white;padding:2px 9px;"
            f"border-radius:10px;font-size:0.72rem;font-weight:600'>{text}</span>")


def _tags(q):
    st.markdown(
        f"{_badge(q['topic'], '#4A4A4A')}&nbsp;"
        f"{_badge(q['level'], LEVEL_COLOR[q['level']])}&nbsp;"
        f"<span style='color:#888;font-size:0.72rem'>{q['subtopic']} · {q['source']}</span>",
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------------ renderers
def _render_reveal(q, key):
    st.markdown(f"**{q['prompt']}**")
    if q.get("hint"):
        with st.expander("Hint"):
            st.markdown(q["hint"])
    if st.toggle("Show worked answer", key=f"rev_{key}"):
        st.markdown(q["worked"])
        st.session_state.answered[q["id"]] = True


def _render_numeric(q, key):
    st.markdown(f"**{q['prompt']}**")
    if q.get("hint"):
        with st.expander("Hint"):
            st.markdown(q["hint"])
    c1, c2 = st.columns([2, 1])
    with c1:
        val = st.number_input(
            f"Your answer ({q['answer_label']}{', ' + q['unit'] if q['unit'] else ''})",
            value=None, step=0.01, format="%.4f", key=f"num_{key}",
            placeholder="type a number",
        )
    with c2:
        st.write("")
        st.write("")
        check = st.button("Check", key=f"chk_{key}", width="stretch")
    if check:
        if val is None:
            st.warning("Enter a number first.")
        elif abs(val - q["answer"]) <= q["tol"]:
            st.success(f"Correct — {q['answer']}{q['unit']}.")
            st.session_state.answered[q["id"]] = True
            st.markdown(q["worked"])
        else:
            st.error("Not quite — check the setup and try again, or open the worked answer.")
            st.session_state.answered[q["id"]] = False
    if st.toggle("Reveal worked answer", key=f"revn_{key}"):
        st.info(f"Answer: **{q['answer']}{q['unit']}**")
        st.markdown(q["worked"])


def _render_mcq(q, key):
    st.markdown(f"**{q['prompt']}**")
    if q.get("hint"):
        with st.expander("Hint"):
            st.markdown(q["hint"])
    choice = st.radio("Select one", q["choices"], index=None, key=f"mcq_{key}")
    if st.button("Check", key=f"chkm_{key}"):
        if choice is None:
            st.warning("Pick an option first.")
        elif q["choices"].index(choice) == q["correct"]:
            st.success("Correct.")
            st.session_state.answered[q["id"]] = True
            st.markdown(q["worked"])
        else:
            st.error(f"Not quite. The answer is: **{q['choices'][q['correct']]}**")
            st.session_state.answered[q["id"]] = False
            st.markdown(q["worked"])


def _render_question(q, key):
    _tags(q)
    if q["fmt"] == "reveal":
        _render_reveal(q, key)
    elif q["fmt"] == "numeric":
        _render_numeric(q, key)
    else:
        _render_mcq(q, key)


# ------------------------------------------------------------------ modes
def _study(pool):
    st.caption(f"{len(pool)} question(s) in this filter. Work top to bottom, or jump around.")
    for i, q in enumerate(pool):
        with st.container(border=True):
            _render_question(q, key=f"study_{q['id']}")


def _quiz(pool):
    ids = [q["id"] for q in pool]
    if st.session_state.quiz_order != ids:
        # filter changed -> rebuild a shuffled run
        st.session_state.quiz_order = ids
        random.shuffle(st.session_state.quiz_order)
        st.session_state.quiz_pos = 0

    order = st.session_state.quiz_order
    if not order:
        st.info("No questions match this filter.")
        return
    pos = st.session_state.quiz_pos
    qmap = {q["id"]: q for q in pool}
    q = qmap[order[pos]]

    st.progress((pos + 1) / len(order), text=f"Question {pos + 1} of {len(order)}")
    with st.container(border=True):
        _render_question(q, key=f"quiz_{q['id']}")

    c1, c2, c3 = st.columns(3)
    if c1.button("◀ Previous", disabled=pos == 0, width="stretch"):
        st.session_state.quiz_pos -= 1
        st.rerun()
    if c2.button("Shuffle again", width="stretch"):
        random.shuffle(st.session_state.quiz_order)
        st.session_state.quiz_pos = 0
        st.rerun()
    if c3.button("Next ▶", disabled=pos >= len(order) - 1, width="stretch"):
        st.session_state.quiz_pos += 1
        st.rerun()


def _flashcards(pool):
    if not pool:
        st.info("No questions match this filter.")
        return
    pos = st.session_state.flash_pos % len(pool)
    q = pool[pos]
    st.caption(f"Card {pos + 1} of {len(pool)}")
    with st.container(border=True):
        _tags(q)
        st.markdown(f"### {q['prompt']}")
        if not st.session_state.flash_show:
            if st.button("Flip to answer", width="stretch"):
                st.session_state.flash_show = True
                st.rerun()
        else:
            if q["fmt"] == "numeric":
                st.info(f"**{q['answer']}{q['unit']}** — {q['answer_label']}")
            elif q["fmt"] == "mcq":
                st.info(f"**{q['choices'][q['correct']]}**")
            st.markdown(q["worked"])
    c1, c2 = st.columns(2)
    if c1.button("◀ Prev card", width="stretch"):
        st.session_state.flash_pos = (pos - 1) % len(pool)
        st.session_state.flash_show = False
        st.rerun()
    if c2.button("Next card ▶", width="stretch"):
        st.session_state.flash_pos = (pos + 1) % len(pool)
        st.session_state.flash_show = False
        st.rerun()


# ------------------------------------------------------------------ entry
def render():
    _init_state()
    st.title("Practice questions")
    st.caption("Interview-style problems in the concept → question → worked-answer format "
               "from your sessions. Numeric answers are graded against the same engine the "
               "calculators use.")

    # progress meter
    total = len(QUESTIONS)
    correct = sum(1 for v in st.session_state.answered.values() if v)
    seen = len(st.session_state.answered)
    m1, m2, m3 = st.columns(3)
    m1.metric("Questions", total)
    m2.metric("Attempted", seen)
    m3.metric("Correct / revealed", correct)
    st.progress(seen / total if total else 0,
                text="Interview-readiness — questions attempted")

    st.divider()

    # filters
    fc1, fc2, fc3, fc4 = st.columns([2, 1.4, 1.4, 1.2])
    topic = fc1.selectbox("Topic", ["All topics"] + TOPICS)
    level = fc2.selectbox("Difficulty", ["All"] + LEVELS)
    fmt_label = fc3.selectbox("Type", ["All"] + list(FORMATS.values()))
    mode = fc4.selectbox("Mode", ["Study", "Quiz", "Flashcards"])

    fmt_key = None
    for k, v in FORMATS.items():
        if v == fmt_label:
            fmt_key = k
    pool = by_topic(
        topic=None if topic == "All topics" else topic,
        level=None if level == "All" else level,
        fmt=fmt_key,
    )

    if st.button("Reset progress", type="secondary"):
        st.session_state.answered = {}
        st.rerun()

    st.divider()
    if mode == "Study":
        _study(pool)
    elif mode == "Quiz":
        _quiz(pool)
    else:
        _flashcards(pool)
