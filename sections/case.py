"""
Thoughtworks / Apax take-private — the capstone.

Students watch the DCF collapse as the forecast deteriorates between the two
Lazard books, then set it against what the deal actually did. The driver model
is an ILLUSTRATIVE reconstruction that reproduces the direction and rough
magnitude of the published per-share ranges; it is not the bank's internal
model. Public deal facts are labelled as such. Swap in the real Session-5
figures / Lazard book pages when finalised.
"""
import pandas as pd
import streamlit as st

from lib import finance as f

# Published per-share DCF ranges from the two sell-side books (from the course notes)
BOOK_2023 = (9.41, 14.94)   # "Triangulation I", May 2023
BOOK_2024 = (4.13, 6.56)    # "Triangulation II", June 2024

# Public deal facts
REJECTED_OFFER = 11.00      # 2023 approach, per share (~$4.0bn EV)
CLOSED_PRICE = 4.40         # closed Nov 2024, per share (~$1.75bn EV)


def _mini_dcf(rev0, g, margin, capex_pct, wacc_, tg, net_debt, shares):
    fc = f.five_year_fcff(rev0, g, margin, 0.25, 0.05, capex_pct, 0.05)
    return f.dcf(fc.fcff, wacc_, tg, net_debt, shares)


def render():
    st.title("Capstone — Thoughtworks take-private")
    st.caption("Apax Partners' take-private of Thoughtworks (NASDAQ: TWKS), advised by "
               "Lazard. The whole course, applied to one deal.")

    st.markdown(
        "Between two sell-side books thirteen months apart, the DCF output "
        f"collapsed from roughly **\\${BOOK_2023[0]:.2f}–\\${BOOK_2023[1]:.2f}** "
        f"(May 2023) to **\\${BOOK_2024[0]:.2f}–\\${BOOK_2024[1]:.2f}** (June 2024) — "
        "not because the method changed, but because the *forecast* did. That gap is the "
        "teaching point: a DCF is only as good as the drivers you feed it.")

    c1, c2 = st.columns(2)
    c1.metric("Rejected 2023 approach", f"${REJECTED_OFFER:.2f}/sh", "≈ $4.0bn EV")
    c2.metric("Closed Nov 2024", f"${CLOSED_PRICE:.2f}/sh", "≈ $1.75bn EV",
              delta_color="inverse")
    st.caption("Both figures matter: the distance between the price first floated and the "
               "price it actually closed at *is* the story.")

    st.divider()
    st.subheader("Deteriorate the forecast, watch the value move")
    st.caption("Illustrative driver model — reproduces the direction and rough magnitude of "
               "the published ranges. Not Lazard's internal model.")

    preset = st.radio("Scenario", ["May 2023 book (optimistic)",
                                   "June 2024 book (deteriorated)", "Custom"],
                      horizontal=True)
    # Calibrated so the default per-share output lands inside each published
    # book range (2023: $9.41-14.94 -> ~$12.2; 2024: $4.13-6.56 -> ~$5.2).
    presets = {
        "May 2023 book (optimistic)": dict(g=0.13, margin=0.13, capex=0.03, wacc=0.115, tg=0.03),
        "June 2024 book (deteriorated)": dict(g=0.02, margin=0.11, capex=0.035, wacc=0.115, tg=0.025),
    }
    base = presets.get(preset, presets["June 2024 book (deteriorated)"])

    c1, c2, c3 = st.columns(3)
    g = c1.slider("Revenue growth", -0.05, 0.25, base["g"], 0.01)
    margin = c1.slider("EBIT margin", 0.02, 0.20, base["margin"], 0.01)
    capex = c2.slider("Capex % of sales", 0.02, 0.08, base["capex"], 0.005)
    wacc_ = c2.slider("WACC", 0.08, 0.16, base["wacc"], 0.005)
    tg = c3.slider("Terminal growth", 0.0, 0.04, base["tg"], 0.005)

    # rough scale to Thoughtworks-like size ($M): ~$1,100M revenue, ~150M shares, ~$400M net debt
    r = _mini_dcf(1100.0, g, margin, capex, wacc_, tg, net_debt=400.0, shares=150.0)
    a, b, c = st.columns(3)
    a.metric("Enterprise Value", f"${r.enterprise_value:,.0f}M")
    b.metric("Equity Value", f"${r.equity_value:,.0f}M")
    c.metric("Value / share", f"${r.per_share:,.2f}")

    band = "within" if BOOK_2024[0] <= r.per_share <= BOOK_2023[1] else "outside"
    st.caption(f"Your per-share sits {band} the two published book ranges. Optimistic "
               "drivers land near the 2023 book; deteriorated drivers near the 2024 book "
               "and the eventual close.")

    st.divider()
    st.subheader("Where it lands vs. the evidence")
    chart_df = pd.DataFrame({
        "$/share": [BOOK_2023[0], BOOK_2023[1], BOOK_2024[0], BOOK_2024[1],
                    CLOSED_PRICE, REJECTED_OFFER, r.per_share],
    }, index=["2023 book low", "2023 book high", "2024 book low", "2024 book high",
              "Closed price", "2023 approach", "Your DCF"])
    st.bar_chart(chart_df)

    with st.expander("Discussion prompts for the session"):
        st.markdown(
            "- Which single driver move does the most damage to per-share value here?\n"
            "- The 2023 approach was rejected as too low, yet the deal closed far below it. "
            "What has to be true about the *forecast* (not the method) for both to make "
            "sense?\n"
            "- If terminal value is a large share of EV, how much of this collapse is "
            "explicit-forecast vs. terminal assumptions?\n"
            "- How would trading comps and precedent transactions have moved over the same "
            "13 months, and would triangulation have caught the deterioration earlier?")

    st.info("Session 5 hook: this is where the real Lazard book pages (football field, "
            "share-price chart, analysis-at-various-prices) slot in as a thin teaching "
            "wrapper. Add your finalised Session-5 figures and the deal will drive itself.")
