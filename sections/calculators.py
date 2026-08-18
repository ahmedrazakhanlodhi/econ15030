"""Interactive calculators — the canonical, consistency-enforcing math.

Every widget carries an explicit `key` so shared labels across tabs never
collide, and layout uses the current `width=` API.
"""
import pandas as pd
import streamlit as st

from lib import finance as f


# ------------------------------------------------------------------ 1. ripple
def _ripple():
    st.subheader("Three-statement ripple")
    st.caption("Pick a change and watch it flow through the income statement, cash flow "
               "statement, and balance sheet — the core 'walk me through' mechanic.")
    scenario = st.radio(
        "Scenario",
        ["Accounts Receivable rises (slower collection)",
         "Extra depreciation (non-cash charge)",
         "Inventory write-down (non-cash charge)"],
        index=0, key="rip_scenario",
    )
    tax = st.slider("Tax rate", 0.0, 0.45, 0.25, 0.01, format="%.2f", key="rip_tax")

    if scenario.startswith("Accounts"):
        amt = st.number_input("A/R increase ($)", value=100.0, step=10.0, key="rip_ar")
        rows = [
            ("Income Statement — Net Income", 0.0, "Revenue & expenses unchanged"),
            ("Cash Flow — CFO (ΔWorking capital)", -amt, "Cash tied up in receivables"),
            ("Balance Sheet — A/R", +amt, "Asset rises"),
            ("Balance Sheet — Cash", -amt, "Asset falls; sheet still balances"),
        ]
        df = pd.DataFrame(rows, columns=["Line", "Change ($)", "Why"])
        st.dataframe(df, hide_index=True, width="stretch")
    else:
        charge = st.number_input("Size of the non-cash charge ($)", value=50.0, step=10.0,
                                 key="rip_charge")
        ni = -charge * (1 - tax)
        cash = charge * tax
        asset_word = "PP&E" if "depreciation" in scenario else "Inventory"
        rows = [
            ("Income Statement — Net Income", ni, f"−charge × (1 − {tax:.0%})"),
            ("Cash Flow — total cash", cash, f"Tax saving = {tax:.0%} × charge (non-cash add-back)"),
            (f"Balance Sheet — {asset_word}", -charge, "Asset written down / depreciated"),
            ("Balance Sheet — Cash", cash, "Rises by the tax saving"),
            ("Balance Sheet — Retained Earnings", ni, "Falls with Net Income"),
        ]
        df = pd.DataFrame(rows, columns=["Line", "Change ($)", "Why"])
        st.dataframe(df, hide_index=True, width="stretch")
        st.info("Check it balances: Assets change "
                f"= {(-charge + cash):+.1f}; Equity change = {ni:+.1f}. Equal ✔")
        st.caption("Assumes the charge is tax-deductible in the period, so it creates a "
                   "cash tax saving. A non-deductible write-down would lower Net Income "
                   "with no cash tax benefit.")


# ------------------------------------------------------------------ 2. fcff
def _fcff_single():
    st.subheader("FCFF builder — the unlevered (NOPAT) route")
    st.caption("The only FCFF definition in the app: NOPAT + D&A − Capex − ΔNWC.")
    c1, c2, c3 = st.columns(3)
    ebit = c1.number_input("EBIT ($M)", value=40.0, step=1.0, key="fcff_ebit")
    tax = c1.number_input("Tax rate", value=0.25, step=0.01, format="%.2f", min_value=0.0, max_value=0.60, key="fcff_tax")
    dna = c2.number_input("D&A ($M)", value=20.0, step=1.0, key="fcff_dna")
    capex = c2.number_input("Capex ($M)", value=35.0, step=1.0, key="fcff_capex")
    d_ar = c3.number_input("Δ A/R ($M)", value=10.0, step=1.0, key="fcff_ar")
    d_inv = c3.number_input("Δ Inventory ($M)", value=5.0, step=1.0, key="fcff_inv")
    d_ap = c3.number_input("Δ A/P ($M)", value=8.0, step=1.0, key="fcff_ap")

    nop = f.nopat(ebit, tax)
    dnwc = f.change_in_nwc(d_ar, d_inv, d_ap)
    fcff = f.fcff(nop, dna, capex, dnwc)

    steps = pd.DataFrame([
        ("NOPAT = EBIT × (1 − t)", nop),
        ("+ D&A", dna),
        ("− Capex", -capex),
        ("− ΔNWC  (ΔA/R + ΔInv − ΔA/P)", -dnwc),
        ("= FCFF", fcff),
    ], columns=["Step", "$M"])
    st.dataframe(steps, hide_index=True, width="stretch")
    st.metric("FCFF (unlevered)", f"${fcff:,.1f}M")

    with st.expander("See the Net-Income (FCFE) trap for these inputs"):
        interest = st.number_input("Interest expense ($M)", value=8.0, step=1.0,
                                   min_value=0.0, key="fcff_int")
        ebt = ebit - interest
        ni = ebt * (1 - tax)
        levered = ni + dna - capex - dnwc
        wedge = fcff - levered
        st.write(f"With interest of {interest:.0f}: EBT = {ebit:.0f} − {interest:.0f} = "
                 f"{ebt:.0f}; Net Income = {ebt:.0f} × (1 − {tax:.0%}) = **{ni:.1f}**.")
        st.write(f"Net-Income route: {ni:.1f} + {dna:.0f} − {capex:.0f} − {dnwc:.0f} = "
                 f"**{levered:.1f}** (a levered / FCFE-style figure).")
        st.write(f"Gap to FCFF = **{wedge:.1f}** = interest × (1 − tax) = "
                 f"{interest:.0f} × {1-tax:.2f} = {interest*(1-tax):.1f}. "
                 "Because we derived Net Income from the same EBIT, interest and tax, the "
                 "gap is *exactly* the after-tax interest — which starting from NOPAT "
                 "avoids entirely.")


# ------------------------------------------------------------------ 3. 5yr
def _five_year():
    st.subheader("Five-year FCFF from drivers")
    c1, c2, c3, c4 = st.columns(4)
    rev0 = c1.number_input("Start revenue ($M)", value=200.0, step=10.0, key="fy_rev")
    g = c1.number_input("Revenue growth", value=0.08, step=0.01, format="%.2f", key="fy_g")
    margin = c2.number_input("EBIT margin", value=0.18, step=0.01, format="%.2f", key="fy_margin")
    tax = c2.number_input("Tax rate", value=0.25, step=0.01, format="%.2f", min_value=0.0, max_value=0.60, key="fy_tax")
    dna = c3.number_input("D&A % of sales", value=0.06, step=0.01, format="%.2f", key="fy_dna")
    capex = c3.number_input("Capex % of sales", value=0.07, step=0.01, format="%.2f", key="fy_capex")
    nwc = c4.number_input("NWC % of sales", value=0.12, step=0.01, format="%.2f", key="fy_nwc")

    fc = f.five_year_fcff(rev0, g, margin, tax, dna, capex, nwc)
    df = pd.DataFrame({
        "Year": fc.years, "Revenue": fc.revenue, "EBIT": fc.ebit, "NOPAT": fc.nopat,
        "+ D&A": fc.dna, "− Capex": fc.capex, "− ΔNWC": fc.delta_nwc, "FCFF": fc.fcff,
    }).set_index("Year").round(1)
    st.dataframe(df.style.format("{:,.1f}"), width="stretch")
    st.bar_chart(pd.DataFrame({"FCFF": fc.fcff}, index=fc.years))
    st.session_state["dcf_stream"] = [round(x, 2) for x in fc.fcff]
    st.caption("This FCFF stream is handed to the DCF Engine tab automatically.")


# ------------------------------------------------------------------ 4. wacc
def _wacc():
    st.subheader("WACC, CAPM & beta")
    st.markdown("**Cost of equity (CAPM)**")
    c1, c2, c3 = st.columns(3)
    rf = c1.number_input("Risk-free rate", value=0.04, step=0.005, format="%.3f", key="w_rf")
    beta = c2.number_input("Beta (levered)", value=1.20, step=0.05, key="w_beta")
    erp = c3.number_input("Equity risk premium", value=0.055, step=0.005, format="%.3f", key="w_erp")
    re = f.capm(rf, beta, erp)
    st.write(f"rₑ = {rf:.3f} + {beta:.2f} × {erp:.3f} = **{re:.3%}**")

    with st.expander("Unlever / re-lever a comparable's beta (Hamada)"):
        b1, b2, b3 = st.columns(3)
        bl = b1.number_input("Comparable levered β", value=1.40, step=0.05, key="w_bl")
        de = b2.number_input("Comparable D/E", value=0.60, step=0.05, key="w_de")
        de_t = b3.number_input("Target D/E", value=0.40, step=0.05, key="w_det")
        tax_b = st.slider("Tax rate (beta)", 0.0, 0.45, 0.25, 0.01, key="w_taxb")
        bu = f.unlever_beta(bl, tax_b, de)
        bl_t = f.relever_beta(bu, tax_b, de_t)
        st.write(f"Unlevered β = {bl:.2f} / [1 + (1−{tax_b:.0%})×{de:.2f}] = **{bu:.3f}**")
        st.write(f"Re-levered β = {bu:.3f} × [1 + (1−{tax_b:.0%})×{de_t:.2f}] = **{bl_t:.3f}**")

    st.divider()
    st.markdown("**WACC**")
    w1, w2, w3 = st.columns(3)
    wd = w1.slider("Debt weight", 0.0, 1.0, 0.40, 0.05, key="w_wd")
    re_in = w2.number_input("Cost of equity", value=round(re, 4), step=0.005, format="%.4f", key="w_re")
    rd = w3.number_input("Pre-tax cost of debt", value=0.06, step=0.005, format="%.3f", key="w_rd")
    tax_w = st.slider("Tax rate (WACC)", 0.0, 0.45, 0.25, 0.01, key="w_taxw")
    we = 1 - wd
    w = f.wacc(we, re_in, wd, rd, tax_w)
    st.write(f"WACC = {we:.0%}×{re_in:.3%} + {wd:.0%}×[{rd:.3%}×(1−{tax_w:.0%})] = **{w:.3%}**")
    st.metric("WACC", f"{w:.2%}")
    st.session_state["dcf_wacc"] = round(w, 4)


# ------------------------------------------------------------------ 5. dcf
def _dcf():
    st.subheader("DCF engine")
    default_stream = st.session_state.get("dcf_stream", [80.0, 90.0, 100.0, 110.0, 120.0])
    txt = st.text_input("FCFF stream ($M, comma-separated)",
                        value=", ".join(f"{x:g}" for x in default_stream), key="dcf_txt")
    try:
        stream = [float(x) for x in txt.split(",") if x.strip()]
    except ValueError:
        st.error("Enter numbers separated by commas.")
        return
    if not stream:
        st.error("Enter at least one FCFF value.")
        return

    c1, c2, c3, c4 = st.columns(4)
    wacc_ = c1.number_input("WACC", value=st.session_state.get("dcf_wacc", 0.084),
                            step=0.005, format="%.4f", key="dcf_wacc_in")
    g = c2.number_input("Terminal growth", value=0.025, step=0.005, format="%.4f", key="dcf_g")
    net_debt = c3.number_input("Net debt ($M)", value=300.0, step=10.0, key="dcf_nd")
    shares = c4.number_input("Diluted shares (M)", value=50.0, step=1.0, min_value=1.0, key="dcf_sh")
    mid = st.toggle("Mid-year convention", value=False, key="dcf_mid")

    if wacc_ <= g:
        st.error("WACC must exceed terminal growth (the TV denominator breaks otherwise).")
        return

    r = f.dcf(stream, wacc_, g, net_debt, shares, mid_year=mid)
    a, b, c = st.columns(3)
    a.metric("Enterprise Value", f"${r.enterprise_value:,.0f}M")
    b.metric("Equity Value", f"${r.equity_value:,.0f}M")
    c.metric("Value / share", f"${r.per_share:,.2f}")

    build = pd.DataFrame([
        ("PV of forecast FCFF", r.pv_fcff),
        ("Terminal value (@ year T)", r.terminal_value),
        ("PV of terminal value", r.pv_terminal),
        ("Enterprise Value", r.enterprise_value),
        ("− Net debt", -net_debt),
        ("Equity Value", r.equity_value),
    ], columns=["Component", "$M"])
    st.dataframe(build, hide_index=True, width="stretch")
    tv_share = r.pv_terminal / r.enterprise_value
    st.caption(f"Terminal value is **{tv_share:.0%}** of EV — "
               + ("watch how much rests on the steady state." if tv_share > 0.7
                  else "a reasonable share."))

    st.markdown("**Sensitivity — Enterprise Value ($M)**")
    st.caption("Terminal FCFF is recomputed for every growth column, so no cell reuses a "
               "stale FCFF₆.")
    waccs = [round(wacc_ + d, 4) for d in (-0.01, -0.005, 0.0, 0.005, 0.01)]
    growths = [round(g + d, 4) for d in (-0.005, 0.0, 0.005)]
    grid = f.ev_sensitivity(stream, waccs, growths)
    sdf = pd.DataFrame(
        {f"g={gg:.1%}": [grid[gg][ww] for ww in waccs] for gg in growths},
        index=[f"WACC {ww:.2%}" for ww in waccs],
    )
    try:
        styled = sdf.style.format("{:,.0f}").background_gradient(cmap="RdYlGn")
        st.dataframe(styled, width="stretch")
    except Exception:
        st.dataframe(sdf.round(0), width="stretch")


# ------------------------------------------------------------------ 6. mult
def _multiples():
    st.subheader("Multiples & the EV→Equity bridge")
    tab1, tab2, tab3 = st.tabs(["Multiple → price", "Price → multiple", "EV → Equity bridge"])
    with tab1:
        c1, c2, c3, c4 = st.columns(4)
        mult = c1.number_input("EV/EBITDA (x)", value=10.0, step=0.5, key="m1_mult")
        ebitda = c2.number_input("EBITDA ($M)", value=100.0, step=5.0, min_value=0.1, key="m1_eb")
        nd = c3.number_input("Net debt ($M)", value=300.0, step=10.0, key="m1_nd")
        sh = c4.number_input("Shares (M)", value=50.0, step=1.0, min_value=1.0, key="m1_sh")
        out = f.share_price_from_multiple(mult, ebitda, nd, sh)
        st.write(f"EV = {mult:g} × {ebitda:g} = **${out['ev']:,.0f}M** → "
                 f"Equity = **${out['equity']:,.0f}M** → "
                 f"Price = **${out['price']:,.2f}**")
    with tab2:
        c1, c2, c3, c4 = st.columns(4)
        px = c1.number_input("Share price ($)", value=20.0, step=1.0, key="m2_px")
        sh2 = c2.number_input("Shares (M)", value=50.0, step=1.0, min_value=1.0, key="m2_sh")
        nd2 = c3.number_input("Net debt ($M)", value=200.0, step=10.0, key="m2_nd")
        eb2 = c4.number_input("EBITDA ($M)", value=100.0, step=5.0, min_value=0.1, key="m2_eb")
        out = f.multiple_from_share_price(px, sh2, nd2, eb2)
        st.write(f"Market cap = **${out['mkt_cap']:,.0f}M** → EV = **${out['ev']:,.0f}M** "
                 f"→ EV/EBITDA = **{out['multiple']:.1f}x**")
    with tab3:
        c1, c2, c3 = st.columns(3)
        ev = c1.number_input("Enterprise Value ($M)", value=2500.0, step=50.0, key="m3_ev")
        gd = c1.number_input("Gross debt ($M)", value=500.0, step=10.0, key="m3_gd")
        xc = c2.number_input("Excess cash ($M)", value=75.0, step=5.0, key="m3_xc")
        sti = c2.number_input("Short-term investments ($M)", value=25.0, step=5.0, key="m3_sti")
        mi = c3.number_input("Minority interest ($M)", value=150.0, step=10.0, key="m3_mi")
        nop = c3.number_input("Non-operating assets ($M)", value=125.0, step=10.0, key="m3_nop")
        eq = f.ev_to_equity(ev, gd, xc, sti, mi, nop)
        st.metric("Equity Value", f"${eq:,.0f}M")
        st.caption("Equity = EV − gross debt + excess cash + ST investments "
                   "− minority interest + non-operating assets.")


# ------------------------------------------------------------------ 7. synergy
def _synergy():
    st.subheader("Synergy value & bidding discipline")
    c1, c2 = st.columns(2)
    annual = c1.number_input("After-tax annual synergy ($M)", value=150.0, step=10.0, key="sy_ann")
    disc = c2.number_input("Discount rate", value=0.08, step=0.005, format="%.3f", min_value=0.001, key="sy_disc")
    shares = c1.number_input("Diluted shares (M)", value=50.0, step=1.0, min_value=1.0, key="sy_sh")
    anchor = c2.number_input("Standalone anchor — DCF high ($/share)", value=58.0, step=1.0, key="sy_anchor")

    val = f.perpetual_synergy_value(annual, disc)
    per_share = val / shares
    ceiling = anchor + per_share
    a, b, c = st.columns(3)
    a.metric("Synergy value", f"${val:,.0f}M")
    b.metric("Synergy / share", f"${per_share:,.2f}")
    c.metric("Ceiling (pay away all)", f"${ceiling:,.2f}")

    keep = st.slider("Share of synergy the buyer keeps", 0.0, 1.0, 0.5, 0.05, key="sy_keep")
    walk = anchor + per_share * (1 - keep)
    st.write(f"Walk-away if buyer keeps {keep:.0%} of synergy = "
             f"${anchor:.0f} + ${per_share:.2f}×{1-keep:.0%} = **${walk:,.2f}**")
    st.caption("Simplified perpetuity (no growth, ramp, or integration cost). The ceiling "
               "is a boundary, not a target.")


# ------------------------------------------------------------------ entry
def render():
    st.title("Calculators")
    st.caption("Every result comes from the same engine that grades the practice "
               "questions — one definition of FCFF, one DCF assembly, everywhere.")
    tabs = st.tabs([
        "3-Statement ripple", "FCFF builder", "5-year FCFF",
        "WACC & beta", "DCF engine", "Multiples & bridge", "Synergy & bidding",
    ])
    with tabs[0]:
        _ripple()
    with tabs[1]:
        _fcff_single()
    with tabs[2]:
        _five_year()
    with tabs[3]:
        _wacc()
    with tabs[4]:
        _dcf()
    with tabs[5]:
        _multiples()
    with tabs[6]:
        _synergy()
