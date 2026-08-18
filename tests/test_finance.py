"""
Numerical tests for the finance engine.

Runs with pytest (`pytest tests/`) or standalone (`python tests/test_finance.py`).
Covers: every worked figure from the four decks, the engine guardrails, and the
capstone preset calibration.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lib import finance as f  # noqa: E402


def _close(a, b, tol):
    assert abs(a - b) <= tol, f"{a} vs {b} (tol {tol})"


# ---------------------------------------------------------------- deck figures
def test_nopat_and_fcff():
    _close(f.nopat(80, 0.25), 60, 0.01)
    dn = f.change_in_nwc(10, 5, 8)
    _close(dn, 7, 0.01)
    _close(f.fcff(f.nopat(40, 0.25), 20, 35, dn), 8, 0.01)
    _close(f.after_tax_interest_wedge(40, 32, 0.25), 6, 0.01)


def test_working_capital_days():
    y1 = f.wc_from_days(500, 350, 45, 60, 30)
    y2 = f.wc_from_days(600, 420, 45, 60, 30)
    _close(y2["nwc"] - y1["nwc"], 18.2, 0.2)


def test_five_year_stream():
    fc = f.five_year_fcff(200, 0.08, 0.18, 0.25, 0.06, 0.07, 0.12)
    _close(fc.revenue[-1], 293.9, 0.3)
    _close(fc.fcff[0], 25.1, 0.3)
    _close(fc.fcff[-1], 34.1, 0.3)


def test_beta_and_wacc():
    bu = f.unlever_beta(1.4, 0.25, 0.6)
    _close(bu, 0.97, 0.01)
    _close(f.relever_beta(bu, 0.25, 0.4), 1.26, 0.01)
    _close(f.wacc(0.6, 0.12, 0.4, 0.06, 0.25), 0.09, 0.001)
    _close(f.wacc(0.6, 0.12, 0.4, 0.06, 0.20), 0.0912, 0.001)
    _close(f.capm(0.04, 1.2, 0.055), 0.106, 0.001)


def test_terminal_and_dcf():
    _close(f.terminal_value(150, 0.03, 0.09), 2575, 1)
    _close(f.terminal_value(150, 0.025, 0.09), 2365, 2)
    r = f.dcf([80, 90, 100, 110, 120], 0.084, 0.025, 300, 50)
    _close(r.pv_fcff, 389, 1)
    _close(r.enterprise_value, 1782, 2)
    _close(r.per_share, 29.63, 0.05)


def test_bridge_multiples_synergy():
    _close(f.ev_to_equity(2500, 500, 75, 25, 150, 125), 2075, 0.5)
    _close(f.share_price_from_multiple(10, 100, 300, 50)["price"], 14.0, 0.01)
    _close(f.multiple_from_share_price(20, 50, 200, 100)["multiple"], 12.0, 0.01)
    _close(f.perpetual_synergy_value(150, 0.08), 1875, 1)


def test_sensitivity_recomputes_terminal_fcff():
    # A higher g must raise EV at fixed WACC — only true if terminal FCFF is
    # recomputed per column rather than held fixed.
    grid = f.ev_sensitivity([80, 90, 100, 110, 120], [0.09], [0.02, 0.03])
    assert grid[0.03][0.09] > grid[0.02][0.09]


# ---------------------------------------------------------------- guardrails
def test_guardrails():
    for bad in (0.09, 0.10, 0.11):
        try:
            f.terminal_value(120, bad, 0.09)  # g >= wacc
            assert False, "expected ValueError"
        except ValueError:
            pass
    try:
        f.perpetual_synergy_value(150, 0.0)
        assert False, "expected ValueError"
    except ValueError:
        pass


# ---------------------------------------------------------------- capstone
def _capstone_ps(g, margin, capex, wacc, tg):
    fc = f.five_year_fcff(1100, g, margin, 0.25, 0.05, capex, 0.05)
    return f.dcf(fc.fcff, wacc, tg, 400, 150).per_share


def test_capstone_presets_land_in_published_ranges():
    ps23 = _capstone_ps(0.13, 0.13, 0.03, 0.115, 0.03)
    ps24 = _capstone_ps(0.02, 0.11, 0.035, 0.115, 0.025)
    assert 9.41 <= ps23 <= 14.94, f"2023 preset ${ps23:.2f} outside book range"
    assert 4.13 <= ps24 <= 6.56, f"2024 preset ${ps24:.2f} outside book range"


# ---------------------------------------------------------------- answer keys
# Every practice answer that maps to a single engine call, re-derived here.
def test_numeric_answer_keys_match_engine():
    from data.questions import QUESTIONS
    qd = {q["id"]: q for q in QUESTIONS}
    checks = {
        "dcf-capm": f.capm(0.04, 1.2, 0.055) * 100,
        "dcf-unlever": f.unlever_beta(1.4, 0.25, 0.6),
        "dcf-relever": f.relever_beta(f.unlever_beta(1.4, 0.25, 0.6), 0.25, 0.4),
        "dcf-atkd": f.after_tax_cost_of_debt(0.075, 0.25) * 100,
        "dcf-wacc": f.wacc(0.6, 0.12, 0.4, 0.06, 0.25) * 100,
        "dcf-wacc-tax": f.wacc(0.6, 0.12, 0.4, 0.06, 0.20) * 100,
        "dcf-wacc-2": f.wacc(0.7, 0.11, 0.3, 0.065, 0.21) * 100,
        "dcf-tv": f.terminal_value(150, 0.03, 0.09),
        "dcf-tv-cap": f.terminal_value(150, 0.025, 0.09),
        "dcf-pv-single": 120 * f.discount_factor(0.09, 5),
        "dcf-assembly-ev": f.dcf([80, 90, 100, 110, 120], 0.084, 0.025, 300, 50).enterprise_value,
        "dcf-assembly-ps": f.dcf([80, 90, 100, 110, 120], 0.084, 0.025, 300, 50).per_share,
        "mult-price": f.share_price_from_multiple(10, 100, 300, 50)["price"],
        "mult-multiple": f.multiple_from_share_price(20, 50, 200, 100)["multiple"],
        "mult-price2": f.share_price_from_multiple(9, 150, 400, 40)["price"],
        "mult-implied-ev": f.implied_ev(11.2, 120),
        "mult-synergy": f.perpetual_synergy_value(150, 0.08),
    }
    for qid, val in checks.items():
        exp, tol = qd[qid]["answer"], qd[qid]["tol"]
        assert abs(val - exp) <= tol, f"{qid}: engine {val:.4g} vs key {exp} (tol {tol})"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"PASS {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"FAIL {t.__name__}: {e}")
    print(f"\n{len(tests) - failed}/{len(tests)} passed")
    sys.exit(1 if failed else 0)
