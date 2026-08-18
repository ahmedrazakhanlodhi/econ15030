"""
Canonical finance engine for ECON 15030.

Every calculator screen AND every numeric practice answer-key call these
functions, so the whole app is guaranteed internally consistent:

  * FCFF is ALWAYS built the unlevered NOPAT way (never the levered
    Net-Income route), so the FCFF=8 vs FCFF=2 confusion cannot reappear.
  * The DCF sensitivity grid RECOMPUTES terminal FCFF for every growth
    scenario, so a growth change never leaves FCFF_{T+1} stale.

Keep new logic here rather than inside a screen, so there is exactly one
place a formula lives.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Sequence


# --------------------------------------------------------------------------
# Operating profit
# --------------------------------------------------------------------------
def nopat(ebit: float, tax_rate: float) -> float:
    """After-tax operating profit. EBIT x (1 - t)."""
    return ebit * (1.0 - tax_rate)


def change_in_nwc(delta_ar: float, delta_inv: float, delta_ap: float) -> float:
    """
    Change in operating net working capital.

    Sign convention (the one the decks standardise on):
      an increase in A/R or Inventory USES cash,
      an increase in A/P PROVIDES cash.
    So  dNWC = dAR + dInv - dAP,  and dNWC is SUBTRACTED in FCFF.
    """
    return delta_ar + delta_inv - delta_ap


def fcff(nopat_: float, dna: float, capex: float, delta_nwc: float) -> float:
    """
    Free Cash Flow to the Firm, the unlevered way:
        FCFF = NOPAT + D&A - Capex - dNWC
    This is the ONLY FCFF definition in the app.
    """
    return nopat_ + dna - capex - delta_nwc


def fcff_from_ebit(ebit: float, tax_rate: float, dna: float,
                   capex: float, delta_nwc: float) -> float:
    return fcff(nopat(ebit, tax_rate), dna, capex, delta_nwc)


def after_tax_interest_wedge(ebit: float, ebt: float, tax_rate: float) -> float:
    """
    The gap between the (wrong) Net-Income route and the (right) NOPAT route.
    Interest = EBIT - EBT; wedge = Interest x (1 - t).
    """
    interest = ebit - ebt
    return interest * (1.0 - tax_rate)


# --------------------------------------------------------------------------
# Working capital from days
# --------------------------------------------------------------------------
def wc_from_days(sales: float, cogs: float, dso: float, dio: float, dpo: float,
                 days_in_year: float = 365.0) -> dict:
    ar = sales * dso / days_in_year
    inv = cogs * dio / days_in_year
    ap = cogs * dpo / days_in_year
    return {"ar": ar, "inv": inv, "ap": ap, "nwc": ar + inv - ap}


# --------------------------------------------------------------------------
# Cost of capital
# --------------------------------------------------------------------------
def capm(rf: float, beta: float, erp: float) -> float:
    """Cost of equity. r_e = r_f + beta x ERP."""
    return rf + beta * erp


def unlever_beta(beta_l: float, tax_rate: float, d_over_e: float) -> float:
    """Hamada unlever. b_u = b_L / [1 + (1 - t) * D/E]."""
    return beta_l / (1.0 + (1.0 - tax_rate) * d_over_e)


def relever_beta(beta_u: float, tax_rate: float, d_over_e_target: float) -> float:
    """Hamada re-lever. b_L = b_u * [1 + (1 - t) * D/E_target]."""
    return beta_u * (1.0 + (1.0 - tax_rate) * d_over_e_target)


def after_tax_cost_of_debt(rd: float, tax_rate: float) -> float:
    return rd * (1.0 - tax_rate)


def wacc(w_e: float, r_e: float, w_d: float, r_d: float, tax_rate: float) -> float:
    """WACC = We*re + Wd*rd*(1 - t)."""
    return w_e * r_e + w_d * after_tax_cost_of_debt(r_d, tax_rate)


# --------------------------------------------------------------------------
# Terminal value & discounting
# --------------------------------------------------------------------------
def terminal_value(fcff_last: float, g: float, wacc_: float) -> float:
    """
    Gordon growth terminal value AT the final forecast year T:
        TV_T = FCFF_T x (1 + g) / (WACC - g)
    Raises if WACC <= g (the formula breaks).
    """
    if wacc_ <= g:
        raise ValueError("WACC must exceed terminal growth g.")
    return fcff_last * (1.0 + g) / (wacc_ - g)


def discount_factor(rate: float, t: int, mid_year: bool = False) -> float:
    exponent = (t - 0.5) if mid_year else t
    return 1.0 / (1.0 + rate) ** exponent


@dataclass
class DCFResult:
    pv_fcff: float
    terminal_value: float
    pv_terminal: float
    enterprise_value: float
    equity_value: float
    per_share: float
    pv_by_year: list = field(default_factory=list)


def dcf(fcff_stream: Sequence[float], wacc_: float, g: float,
        net_debt: float = 0.0, shares: float = 0.0,
        mid_year: bool = False) -> DCFResult:
    """
    Full DCF assembly. Terminal value is discounted from year T (the last
    explicit year), consistent with the decks.
    """
    n = len(fcff_stream)
    pv_by_year = [cf * discount_factor(wacc_, t, mid_year)
                  for t, cf in enumerate(fcff_stream, start=1)]
    pv_fcff = sum(pv_by_year)
    tv = terminal_value(fcff_stream[-1], g, wacc_)
    pv_tv = tv * discount_factor(wacc_, n, mid_year)
    ev = pv_fcff + pv_tv
    equity = ev - net_debt
    per_share = equity / shares if shares else float("nan")
    return DCFResult(pv_fcff, tv, pv_tv, ev, equity, per_share, pv_by_year)


def ev_sensitivity(fcff_stream: Sequence[float], waccs: Sequence[float],
                   growths: Sequence[float], mid_year: bool = False) -> dict:
    """
    Enterprise-value grid over (WACC, g). CRUCIAL: terminal FCFF is
    recomputed inside dcf() for every g, so no scenario reuses a stale
    FCFF_{T+1}. Returns {g: {wacc: EV}}.
    """
    grid = {}
    for g in growths:
        row = {}
        for w in waccs:
            try:
                row[w] = dcf(fcff_stream, w, g, mid_year=mid_year).enterprise_value
            except ValueError:
                row[w] = float("nan")
        grid[g] = row
    return grid


# --------------------------------------------------------------------------
# Driver-based 5-year FCFF build
# --------------------------------------------------------------------------
@dataclass
class DriverForecast:
    years: list
    revenue: list
    ebit: list
    nopat: list
    dna: list
    capex: list
    delta_nwc: list
    fcff: list


def five_year_fcff(start_revenue: float, growth, ebit_margin: float,
                   tax_rate: float, dna_pct: float, capex_pct: float,
                   nwc_pct: float, n: int = 5) -> DriverForecast:
    """
    Build an n-year FCFF stream from operating drivers.
    `growth` may be a scalar (flat) or a list of per-year rates.
    NWC is modelled as a % of sales; dNWC is the year-on-year change.
    """
    if isinstance(growth, (int, float)):
        growth = [growth] * n

    rev, prev_rev = [], start_revenue
    for t in range(n):
        prev_rev = prev_rev * (1.0 + growth[t])
        rev.append(prev_rev)

    ebit = [r * ebit_margin for r in rev]
    nop = [nopat(e, tax_rate) for e in ebit]
    dna = [r * dna_pct for r in rev]
    capex = [r * capex_pct for r in rev]

    nwc_level = [r * nwc_pct for r in rev]
    prev_nwc = start_revenue * nwc_pct
    dnwc = []
    for level in nwc_level:
        dnwc.append(level - prev_nwc)
        prev_nwc = level

    fc = [fcff(nop[t], dna[t], capex[t], dnwc[t]) for t in range(n)]
    return DriverForecast(list(range(1, n + 1)), rev, ebit, nop, dna, capex, dnwc, fc)


# --------------------------------------------------------------------------
# Multiples, the bridge, synergies
# --------------------------------------------------------------------------
def implied_ev(multiple: float, metric: float) -> float:
    return multiple * metric


def share_price_from_multiple(multiple: float, metric: float,
                              net_debt: float, shares: float) -> dict:
    ev = implied_ev(multiple, metric)
    equity = ev - net_debt
    return {"ev": ev, "equity": equity, "price": equity / shares}


def multiple_from_share_price(price: float, shares: float, net_debt: float,
                              metric: float) -> dict:
    mkt_cap = price * shares
    ev = mkt_cap + net_debt
    return {"mkt_cap": mkt_cap, "ev": ev, "multiple": ev / metric}


def ev_to_equity(ev: float, gross_debt: float = 0.0, excess_cash: float = 0.0,
                 st_investments: float = 0.0, minority_interest: float = 0.0,
                 non_operating: float = 0.0) -> float:
    """Equity = EV - gross debt + excess cash + ST inv - minority + non-op."""
    return (ev - gross_debt + excess_cash + st_investments
            - minority_interest + non_operating)


def perpetual_synergy_value(annual_after_tax: float, discount_rate: float) -> float:
    """Simplified: annual / r. (No growth, no ramp, no integration cost.)"""
    return annual_after_tax / discount_rate
