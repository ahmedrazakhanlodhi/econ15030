"""
Practice question bank for ECON 15030.

Each question is a dict. Shared keys:
    id        unique slug
    topic     "Accounting" | "FCFF & Drivers" | "WACC & DCF" | "Multiples & Deals"
    subtopic  short label
    level     "Core" | "Stretch" | "Interview-hard"
    fmt       "reveal" | "numeric" | "mcq"
    prompt    the question (markdown ok)
    hint      optional nudge
    worked    the model answer (markdown)
    source    where it maps in the decks

numeric adds:  answer (float, in the unit stated), unit, tol, answer_label
mcq adds:      choices (list[str]), correct (int index)

Numeric answers were cross-checked against lib/finance.py (see tests at bottom
of this file: run `python data/questions.py`).
"""

QUESTIONS = [
    # ================================================================
    # ACCOUNTING (Lecture 1)
    # ================================================================
    {
        "id": "acc-ar-walk", "topic": "Accounting", "subtopic": "3-statement linkages",
        "level": "Core", "fmt": "reveal", "source": "Lecture 1, slides 11-12",
        "prompt": "Holding revenue and expenses constant, Accounts Receivable rises by "
                  "$100 because customers pay more slowly. Walk me through the impact on "
                  "all three statements.",
        "hint": "A/R is revenue earned but not yet collected in cash. Same sales, more "
                "cash tied up.",
        "worked": "**Income Statement** — no impact. Revenue and expenses are held "
                  "constant, so Net Income is unchanged ($0).\n\n"
                  "**Cash Flow Statement** — CFO falls by **$100** through the change in "
                  "working capital: cash is tied up in receivables.\n\n"
                  "**Balance Sheet** — A/R **+$100**, Cash **-$100**. The sheet still "
                  "balances because both moves are inside assets.\n\n"
                  "*They're testing linkages, not the original sale. The CFS shows the "
                  "cash hit; the balance sheet nets to zero on the asset side.*",
    },
    {
        "id": "acc-accel-walk", "topic": "Accounting", "subtopic": "Depreciation",
        "level": "Core", "fmt": "reveal", "source": "Lecture 1, slides 13-15",
        "prompt": "A company switches from straight-line to accelerated depreciation, so "
                  "Year-1 D&A is $50 higher. Tax rate 25%, and the higher depreciation is "
                  "tax-deductible. Walk through the Year-1 impact on all three statements.",
        "hint": "Extra non-cash expense lowers book profit but saves cash taxes now.",
        "worked": "**Income Statement** — D&A +$50 ⇒ EBIT -$50 ⇒ tax -$12.5 (25%×50) ⇒ "
                  "**Net Income -$37.5**.\n\n"
                  "**Cash Flow Statement** — start at NI -$37.5, add back non-cash D&A +$50 "
                  "⇒ **CFO +$12.5**. No investing/financing effect ⇒ total cash +$12.5.\n\n"
                  "**Balance Sheet** — PP&E -$50 (faster), Cash +$12.5, Retained Earnings "
                  "-$37.5. Assets -$37.5 = Equity -$37.5, so it balances.\n\n"
                  "*Accelerated depreciation shifts deductions forward: lower taxes now, "
                  "higher later.*",
    },
    {
        "id": "acc-accel-ni", "topic": "Accounting", "subtopic": "Depreciation",
        "level": "Core", "fmt": "numeric", "source": "Lecture 1, slide 14",
        "prompt": "Year-1 D&A is $50 higher (accelerated), tax rate 25%. By how much does "
                  "**Net Income fall**? Enter a positive number of dollars.",
        "hint": "Only the after-tax portion of the extra expense hits Net Income.",
        "answer": 37.5, "unit": "$", "tol": 0.1, "answer_label": "Fall in Net Income",
        "worked": "Extra pre-tax expense $50 × (1 − 0.25) = **$37.5**. Taxes absorb the "
                  "other $12.5.",
    },
    {
        "id": "acc-accel-cash", "topic": "Accounting", "subtopic": "Depreciation",
        "level": "Core", "fmt": "numeric", "source": "Lecture 1, slide 15",
        "prompt": "Same switch: Year-1 D&A is $50 higher, tax 25%. By how much does "
                  "**total cash change** in Year 1? Use + for an increase.",
        "hint": "Non-cash expense, but the tax bill is real.",
        "answer": 12.5, "unit": "$", "tol": 0.1, "answer_label": "Change in cash",
        "worked": "The only cash effect is the tax saving: 25% × $50 = **+$12.5**.",
    },
    {
        "id": "acc-opfin", "topic": "Accounting", "subtopic": "Operating vs financing",
        "level": "Core", "fmt": "mcq", "source": "Lecture 1, slides 16-17",
        "prompt": "You're valuing a firm with $50M cash, $200M inventory, $100M debt, and "
                  "$75M accounts payable. Which pair is **operating** (inside EV)?",
        "choices": ["Cash and Debt", "Inventory and Accounts Payable",
                    "Cash and Inventory", "Debt and Accounts Payable"],
        "correct": 1,
        "hint": "Operating items drive the cash flows behind EV; cash and debt live in the "
                "EV→Equity bridge.",
        "worked": "**Inventory and Accounts Payable** are operating — they move free cash "
                  "flow through working capital (inventory uses cash, payables provide it). "
                  "Cash and debt are financing/non-operating and are handled *after* EV, in "
                  "the bridge to Equity Value.",
    },
    {
        "id": "acc-is-ni", "topic": "Accounting", "subtopic": "Income statement",
        "level": "Core", "fmt": "numeric", "source": "Lecture 1, slide 4",
        "prompt": "Revenue $1,000, COGS $600, SG&A $250, D&A $30, interest $20, tax $25. "
                  "What is **Net Income**?",
        "hint": "Work down to EBIT first, then interest, then the given tax.",
        "answer": 75, "unit": "$", "tol": 0.5, "answer_label": "Net Income",
        "worked": "EBIT = 1000 − 600 − 250 − 30 = 120. EBT = 120 − 20 = 100. "
                  "NI = 100 − 25 = **$75**.",
    },
    {
        "id": "acc-ebitda", "topic": "Accounting", "subtopic": "EBITDA",
        "level": "Core", "fmt": "numeric", "source": "Lecture 1, slide 5",
        "prompt": "Revenue $1,000, COGS $600, SG&A $250, D&A $30. What is **EBITDA**?",
        "hint": "EBITDA is before D&A.",
        "answer": 150, "unit": "$", "tol": 0.5, "answer_label": "EBITDA",
        "worked": "EBITDA = 1000 − 600 − 250 = **$150** (D&A is added back / never "
                  "subtracted). Note EBITDA ≠ cash flow — it ignores taxes, capex and "
                  "working capital.",
    },
    {
        "id": "acc-writedown", "topic": "Accounting", "subtopic": "Non-cash charges",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 1 method",
        "prompt": "A firm takes a $40 inventory write-down (tax-deductible, 25% rate). By "
                  "how much does **Net Income fall**? Enter a positive number.",
        "hint": "Same mechanic as extra depreciation — a non-cash charge, tax-shielded.",
        "answer": 30, "unit": "$", "tol": 0.1, "answer_label": "Fall in Net Income",
        "worked": "$40 × (1 − 0.25) = **$30**. Cash actually *rises* $10 from the tax "
                  "saving, since the write-down itself is non-cash.",
    },
    {
        "id": "acc-cfo-ap", "topic": "Accounting", "subtopic": "Working capital",
        "level": "Core", "fmt": "mcq", "source": "Lecture 1, slide 10",
        "prompt": "Holding profit constant, which change **increases** cash from "
                  "operations?",
        "choices": ["A rise in Accounts Receivable", "A rise in Inventory",
                    "A rise in Accounts Payable", "A rise in PP&E"],
        "correct": 2,
        "hint": "A source of cash is a liability you're stretching.",
        "worked": "**A rise in Accounts Payable** — you're holding onto supplier cash "
                  "longer, a source of cash. Rising A/R and inventory *use* cash; PP&E is "
                  "an investing item, not CFO.",
    },
    {
        "id": "acc-dnwc", "topic": "Accounting", "subtopic": "Working capital",
        "level": "Core", "fmt": "numeric", "source": "Lecture 1 / Lecture 2 sign rule",
        "prompt": "In a period A/R rises $30, Inventory rises $20, and A/P rises $15. What "
                  "is the **change in net working capital** (the amount subtracted in "
                  "FCFF)?",
        "hint": "ΔNWC = ΔA/R + ΔInventory − ΔA/P.",
        "answer": 35, "unit": "$", "tol": 0.1, "answer_label": "ΔNWC",
        "worked": "ΔNWC = 30 + 20 − 15 = **$35**. That's a $35 cash *use*, subtracted in "
                  "FCFF.",
    },
    {
        "id": "acc-deferred-rev", "topic": "Accounting", "subtopic": "Classification",
        "level": "Stretch", "fmt": "mcq", "source": "Lecture 1 concept",
        "prompt": "How should deferred revenue be treated when valuing operations?",
        "choices": ["A financing liability, handled in the bridge",
                    "An operating liability inside working capital",
                    "A non-operating asset added after EV",
                    "Equity, since it belongs to shareholders"],
        "correct": 1,
        "hint": "Cash received before the good/service is delivered.",
        "worked": "It's an **operating liability** — cash collected in advance of earning "
                  "revenue, so it sits in working capital and affects FCFF, not the "
                  "financing bridge.",
    },
    {
        "id": "acc-paydown", "topic": "Accounting", "subtopic": "3-statement linkages",
        "level": "Stretch", "fmt": "reveal", "source": "Lecture 1 method",
        "prompt": "A company uses $100 of cash to pay down debt. Walk through the "
                  "immediate impact on all three statements.",
        "hint": "This is a financing move — no P&L hit on the day it happens.",
        "worked": "**Income Statement** — no immediate impact (interest expense falls in "
                  "*future* periods, lowering future taxes).\n\n"
                  "**Cash Flow Statement** — Financing outflow **-$100**.\n\n"
                  "**Balance Sheet** — Cash -$100, Debt -$100. Assets and "
                  "liabilities both fall by $100, so it balances.",
    },

    # ================================================================
    # FCFF & DRIVERS (Lecture 2)
    # ================================================================
    {
        "id": "fcff-saas-rev", "topic": "FCFF & Drivers", "subtopic": "Revenue",
        "level": "Core", "fmt": "reveal", "source": "Lecture 2, slides 5-6",
        "prompt": "A SaaS company grew 40% last year but faces rising competition and "
                  "saturation. The CEO projects 35% next year. How would you model the "
                  "5-year revenue trajectory, and why?",
        "hint": "Taper the path and tie each year to a business reason.",
        "worked": "Model **below** guidance with a tapering path, e.g. 25% → 18% → 12% → "
                  "8% → 5%, each tied to a story: still-high growth, competition intensifies, "
                  "saturation, approaching mature SaaS, steady-state recurring revenue.\n\n"
                  "*Tapering avoids a heroic Year-5 jump that wrecks terminal-value "
                  "credibility, and a conservative path protects the valuation. The signal "
                  "the interviewer wants: each number linked to the business, not plugged in.*",
    },
    {
        "id": "fcff-nopat", "topic": "FCFF & Drivers", "subtopic": "NOPAT",
        "level": "Core", "fmt": "numeric", "source": "Lecture 2, slides 8-9",
        "prompt": "EBIT $80M, tax rate 25%. What is **NOPAT**?",
        "hint": "NOPAT = EBIT × (1 − tax).",
        "answer": 60, "unit": "$M", "tol": 0.1, "answer_label": "NOPAT",
        "worked": "80 × (1 − 0.25) = **$60M**. This is after-tax operating profit, before "
                  "reinvestment — the right unlevered starting point for FCFF.",
    },
    {
        "id": "fcff-nopat-da", "topic": "FCFF & Drivers", "subtopic": "NOPAT",
        "level": "Core", "fmt": "numeric", "source": "Lecture 2, slide 9",
        "prompt": "NOPAT is $60M and D&A is $15M. What is NOPAT + D&A (the pre-reinvestment "
                  "operating cash base)?",
        "hint": "Add back the non-cash charge.",
        "answer": 75, "unit": "$M", "tol": 0.1, "answer_label": "NOPAT + D&A",
        "worked": "60 + 15 = **$75M**. D&A lowered taxable income but required no cash "
                  "today — the cash went out when the asset was bought. Still not FCFF: "
                  "capex and ΔNWC come next.",
    },
    {
        "id": "fcff-wc-days", "topic": "FCFF & Drivers", "subtopic": "Working capital",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 2, slides 12-13",
        "prompt": "Sales grow from $500M to $600M. A/R = 45 days of sales, Inventory = 60 "
                  "days of COGS, A/P = 30 days of COGS, COGS = 70% of sales. What is the "
                  "**increase in net working capital** (the FCF drag)?",
        "hint": "Build A/R, Inventory, A/P for each year, take NWC = A/R + Inv − A/P, "
                "then the change.",
        "answer": 18.1, "unit": "$M", "tol": 0.4, "answer_label": "ΔNWC",
        "worked": "COGS: 350 → 420. Y1 NWC = 61.6 + 57.5 − 28.8 = 90.3; Y2 NWC = 74.0 + "
                  "69.0 − 34.5 = 108.5. ΔNWC ≈ **+$18.2M** — growth ties up ~18% of "
                  "incremental sales in working capital, a real drag on near-term FCFF.",
    },
    {
        "id": "fcff-lemon", "topic": "FCFF & Drivers", "subtopic": "FCFF build",
        "level": "Core", "fmt": "numeric", "source": "Lecture 2, slides 16-18",
        "prompt": "Lemonade Stand Co. ($M): EBIT 40, tax 25%, D&A 20, Capex 35, ΔA/R +10, "
                  "ΔInventory +5, ΔA/P +8. Compute **FCFF**.",
        "hint": "ΔNWC = 10 + 5 − 8. NOPAT = 40 × 0.75. Then NOPAT + D&A − Capex − ΔNWC.",
        "answer": 8, "unit": "$M", "tol": 0.1, "answer_label": "FCFF",
        "worked": "ΔNWC = 10 + 5 − 8 = 7. NOPAT = 40 × 0.75 = 30. "
                  "FCFF = 30 + 20 − 35 − 7 = **$8M**.\n\n"
                  "*EBITDA here is 60, but FCFF is only 8 — capex and working capital "
                  "absorb most of the cash.*",
    },
    {
        "id": "fcff-lemon-trap", "topic": "FCFF & Drivers", "subtopic": "FCFF vs FCFE",
        "level": "Interview-hard", "fmt": "numeric", "source": "Lecture 2, slide 18",
        "prompt": "Same Lemonade Stand Co., but Net Income is $24M. If you (wrongly) start "
                  "FCFF from Net Income (24 + D&A − Capex − ΔNWC), what figure do you get — "
                  "and what does the gap represent?",
        "hint": "This is the levered/FCFE-style trap. The wedge is after-tax interest.",
        "answer": 2, "unit": "$M", "tol": 0.1, "answer_label": "Net-Income route figure",
        "worked": "24 + 20 − 35 − 7 = **$2M** — a levered, FCFE-style number, *not* FCFF. "
                  "The $6 gap to the correct $8 is after-tax interest: EBIT 40 − EBT 32 = "
                  "$8 interest; $8 × (1 − 25%) = $6. **Always start from NOPAT/EBIT so the "
                  "figure is unlevered from the outset.**",
    },
    {
        "id": "fcff-generic", "topic": "FCFF & Drivers", "subtopic": "FCFF build",
        "level": "Core", "fmt": "numeric", "source": "Lecture 2, slide 14",
        "prompt": "EBIT $200M, tax 30%, D&A $40M, Capex $60M, ΔNWC $25M. Compute FCFF.",
        "hint": "NOPAT first, then the unlevered bridge.",
        "answer": 95, "unit": "$M", "tol": 0.1, "answer_label": "FCFF",
        "worked": "NOPAT = 200 × 0.70 = 140. FCFF = 140 + 40 − 60 − 25 = **$95M**.",
    },
    {
        "id": "fcff-negative", "topic": "FCFF & Drivers", "subtopic": "Sanity checks",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 2, slide 20",
        "prompt": "NOPAT $50M, D&A $10M, Capex $90M, ΔNWC $20M. Compute FCFF, then say in "
                  "one line what you'd investigate.",
        "hint": "Heavy capex can push FCFF negative — growth or trouble?",
        "answer": -50, "unit": "$M", "tol": 0.1, "answer_label": "FCFF",
        "worked": "FCFF = 50 + 10 − 90 − 20 = **−$50M**. Negative FCFF with positive "
                  "operating profit usually flags heavy reinvestment — investigate whether "
                  "the capex is capacity expansion (fine) or a structural problem.",
    },
    {
        "id": "fcff-5yr-y1", "topic": "FCFF & Drivers", "subtopic": "5-year build",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 2, slide 19",
        "prompt": "Start revenue $200M, growth 8%, EBIT margin 18%, tax 25%, D&A 6% of "
                  "sales, Capex 7% of sales, NWC 12% of sales. What is **Year-1 FCFF**?",
        "hint": "Revenue₁ = 216. Build EBIT→NOPAT, add D&A, subtract capex and the change "
                "in NWC (NWC₁ − NWC₀).",
        "answer": 25.1, "unit": "$M", "tol": 0.3, "answer_label": "Year-1 FCFF",
        "worked": "Rev₁ = 216; EBIT = 38.9; NOPAT = 29.2; +D&A 13.0; −Capex 15.1; "
                  "−ΔNWC (25.9 − 24.0 = 1.9) ⇒ FCFF₁ ≈ **$25.1M**.",
    },
    {
        "id": "fcff-ap-driver", "topic": "FCFF & Drivers", "subtopic": "Working capital",
        "level": "Core", "fmt": "mcq", "source": "Lecture 2, slide 20",
        "prompt": "Accounts Payable is best modelled as a percentage of…",
        "choices": ["Sales", "COGS", "EBIT", "Total assets"],
        "correct": 1,
        "hint": "Payables fund purchases from suppliers.",
        "worked": "**COGS.** Payables fund supplier purchases, which scale with cost of "
                  "goods, not with top-line sales.",
    },
    {
        "id": "fcff-why-nopat", "topic": "FCFF & Drivers", "subtopic": "FCFF vs FCFE",
        "level": "Core", "fmt": "reveal", "source": "Lecture 2, slides 7, 15",
        "prompt": "Why does FCFF start from NOPAT rather than Net Income?",
        "hint": "Think about who the cash flow belongs to.",
        "worked": "FCFF is cash available to **all** capital providers (debt + equity), so "
                  "it must be *before* financing effects. NOPAT = EBIT × (1 − t) is already "
                  "unlevered. Net Income is *after* interest — it has already paid debt "
                  "holders — so starting there produces a levered (FCFE-style) figure "
                  "unless you add back after-tax interest.",
    },

    # ================================================================
    # WACC & DCF (Lecture 3)
    # ================================================================
    {
        "id": "dcf-capm", "topic": "WACC & DCF", "subtopic": "Cost of equity",
        "level": "Core", "fmt": "numeric", "source": "Lecture 3, slide 4",
        "prompt": "Risk-free rate 4.0%, beta 1.2, equity risk premium 5.5%. What is the "
                  "**cost of equity**? Enter a percent, e.g. 10.6.",
        "hint": "CAPM: rₑ = r_f + β × ERP.",
        "answer": 10.6, "unit": "%", "tol": 0.05, "answer_label": "Cost of equity",
        "worked": "4.0 + 1.2 × 5.5 = 4.0 + 6.6 = **10.6%**.",
    },
    {
        "id": "dcf-unlever", "topic": "WACC & DCF", "subtopic": "Beta",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 3, slides 7-8",
        "prompt": "A comparable has levered beta 1.40, D/E 0.6, tax 25%. What is its "
                  "**unlevered beta**?",
        "hint": "β_u = β_L / [1 + (1 − t)·D/E].",
        "answer": 0.97, "unit": "", "tol": 0.02, "answer_label": "Unlevered beta",
        "worked": "1.40 / [1 + 0.75 × 0.6] = 1.40 / 1.45 = **0.97**. This strips out the "
                  "comparable's leverage to leave pure business risk.",
    },
    {
        "id": "dcf-relever", "topic": "WACC & DCF", "subtopic": "Beta",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 3, slides 7-8",
        "prompt": "Unlevered beta 0.97. Re-lever to a target D/E of 0.4 at a 25% tax rate. "
                  "What levered beta do you use?",
        "hint": "β_L = β_u × [1 + (1 − t)·D/E_target].",
        "answer": 1.26, "unit": "", "tol": 0.02, "answer_label": "Re-levered beta",
        "worked": "0.97 × [1 + 0.75 × 0.4] = 0.97 × 1.30 = **1.26**. You can't use the "
                  "comparable's 1.40 directly — it embeds *its* capital structure, not the "
                  "target's. Use market values for D/E.",
    },
    {
        "id": "dcf-atkd", "topic": "WACC & DCF", "subtopic": "Cost of debt",
        "level": "Core", "fmt": "numeric", "source": "Lecture 3, slides 10-11",
        "prompt": "A bond yields 7.5% (current YTM). Tax rate 25%. What is the **after-tax "
                  "cost of debt**? Enter a percent.",
        "hint": "Use the current market yield, then apply the tax shield.",
        "answer": 5.625, "unit": "%", "tol": 0.02, "answer_label": "After-tax cost of debt",
        "worked": "7.5% × (1 − 0.25) = **5.625%**. Use the current YTM (7.5%), not the "
                  "historical coupon/‌face rate of 7.0% — a DCF discounts at *today's* cost "
                  "of capital.",
    },
    {
        "id": "dcf-wacc", "topic": "WACC & DCF", "subtopic": "WACC",
        "level": "Core", "fmt": "numeric", "source": "Lecture 3, slides 13-14",
        "prompt": "Cost of equity 12%, cost of debt 6%, tax 25%, target structure 40% "
                  "debt / 60% equity. Compute **WACC**. Enter a percent.",
        "hint": "WACC = Wₑrₑ + W_d·r_d·(1 − t).",
        "answer": 9.0, "unit": "%", "tol": 0.03, "answer_label": "WACC",
        "worked": "0.6 × 12% + 0.4 × [6% × 0.75] = 7.2% + 0.4 × 4.5% = 7.2% + 1.8% = **9.0%**.",
    },
    {
        "id": "dcf-wacc-tax", "topic": "WACC & DCF", "subtopic": "WACC",
        "level": "Interview-hard", "fmt": "numeric", "source": "Lecture 3, slide 14",
        "prompt": "Same inputs (rₑ 12%, r_d 6%, 40/60 D/E). If the tax rate **falls** to "
                  "20%, what is the new WACC? Enter a percent.",
        "hint": "A lower tax rate shrinks the debt tax shield.",
        "answer": 9.12, "unit": "%", "tol": 0.03, "answer_label": "WACC at t = 20%",
        "worked": "After-tax debt = 6% × 0.80 = 4.8%. WACC = 0.6 × 12% + 0.4 × 4.8% = "
                  "**9.12%**. Counter-intuitively, a *lower* tax rate *raises* WACC — the "
                  "shield is worth less.",
    },
    {
        "id": "dcf-wacc-2", "topic": "WACC & DCF", "subtopic": "WACC",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 3, slide 12",
        "prompt": "Weights 70% equity / 30% debt, cost of equity 11%, cost of debt 6.5%, "
                  "tax 21%. Compute WACC. Enter a percent.",
        "hint": "Tax-adjust only the debt leg.",
        "answer": 9.24, "unit": "%", "tol": 0.05, "answer_label": "WACC",
        "worked": "0.70 × 11% + 0.30 × [6.5% × 0.79] = 7.70% + 0.30 × 5.135% = 7.70% + "
                  "1.54% = **9.24%**.",
    },
    {
        "id": "dcf-tv", "topic": "WACC & DCF", "subtopic": "Terminal value",
        "level": "Core", "fmt": "numeric", "source": "Lecture 3, slides 17-18",
        "prompt": "Year-5 FCFF $150M, WACC 9%, terminal growth 3%. Compute the **terminal "
                  "value** (at year 5).",
        "hint": "TV = FCFF₅ × (1 + g) / (WACC − g).",
        "answer": 2575, "unit": "$M", "tol": 3, "answer_label": "Terminal value",
        "worked": "150 × 1.03 / (0.09 − 0.03) = 154.5 / 0.06 = **$2,575M**.",
    },
    {
        "id": "dcf-tv-cap", "topic": "WACC & DCF", "subtopic": "Terminal value",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 3, slide 18",
        "prompt": "Your MD says long-run nominal growth for this market is 2.5%, not 3%. "
                  "Recompute the terminal value capping g at 2.5% (FCFF₅ $150M, WACC 9%).",
        "hint": "Same formula, g = 2.5%.",
        "answer": 2365, "unit": "$M", "tol": 5, "answer_label": "Terminal value (capped)",
        "worked": "150 × 1.025 / (0.09 − 0.025) = 153.75 / 0.065 ≈ **$2,365M**. A 0.5-point "
                  "cut in g moves TV by ~$210M — terminal growth is never a rounding "
                  "decision.",
    },
    {
        "id": "dcf-pv-single", "topic": "WACC & DCF", "subtopic": "Discounting",
        "level": "Core", "fmt": "numeric", "source": "Lecture 3, slide 19",
        "prompt": "What is the present value of $120M received in Year 5 at a 9% WACC "
                  "(end-year convention)?",
        "hint": "PV = CF / (1 + WACC)^t.",
        "answer": 77.99, "unit": "$M", "tol": 0.3, "answer_label": "PV",
        "worked": "120 / 1.09⁵ = 120 / 1.5386 = **$78.0M**.",
    },
    {
        "id": "dcf-assembly-ev", "topic": "WACC & DCF", "subtopic": "DCF assembly",
        "level": "Interview-hard", "fmt": "numeric", "source": "Lecture 3, slides 21-22",
        "prompt": "FCFF (Y1–Y5) = 80, 90, 100, 110, 120 ($M). WACC 8.4%, terminal growth "
                  "2.5%, end-year discounting. What is **Enterprise Value**?",
        "hint": "PV the five flows, add TV = 120×1.025/(0.084−0.025) discounted 5 years.",
        "answer": 1782, "unit": "$M", "tol": 5, "answer_label": "Enterprise Value",
        "worked": "PV of FCFF ≈ $389M. TV = 123.0 / 0.059 = $2,085M; PV(TV) = 2,085 / "
                  "1.084⁵ = $1,393M. EV = 389 + 1,393 = **$1,782M**.",
    },
    {
        "id": "dcf-assembly-ps", "topic": "WACC & DCF", "subtopic": "DCF assembly",
        "level": "Interview-hard", "fmt": "numeric", "source": "Lecture 3, slide 22",
        "prompt": "Continuing: EV $1,782M, net debt $300M, 50M diluted shares. What is the "
                  "**intrinsic value per share**?",
        "hint": "EV − net debt = equity; ÷ shares.",
        "answer": 29.63, "unit": "$", "tol": 0.1, "answer_label": "Value per share",
        "worked": "Equity = 1,782 − 300 = $1,482M. Per share = 1,482 / 50 = **$29.63**.",
    },
    {
        "id": "dcf-tv-share", "topic": "WACC & DCF", "subtopic": "Diagnostics",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 3, slide 26",
        "prompt": "In that DCF, PV of terminal value is $1,393M and Enterprise Value is "
                  "$1,782M. What share of EV is the terminal value? Enter a percent.",
        "hint": "A high share means the answer leans heavily on terminal assumptions.",
        "answer": 78.2, "unit": "%", "tol": 1.0, "answer_label": "TV as % of EV",
        "worked": "1,393 / 1,782 = **78%**. When terminal value is this large a share, "
                  "stress-test g, terminal margin and ROIC — the DCF is mostly a bet on the "
                  "steady state.",
    },
    {
        "id": "dcf-reinvest", "topic": "WACC & DCF", "subtopic": "Consistency check",
        "level": "Interview-hard", "fmt": "numeric", "source": "Lecture 3, slide 16",
        "prompt": "Terminal growth is 2.5% and terminal ROIC is 12.5%. What **reinvestment "
                  "rate** does that imply? Enter a percent.",
        "hint": "g = ROIC × reinvestment rate.",
        "answer": 20, "unit": "%", "tol": 0.5, "answer_label": "Reinvestment rate",
        "worked": "RR = g / ROIC = 2.5% / 12.5% = **20%**. Your terminal growth *implies* "
                  "reinvestment; the two must agree, or the terminal cash flow is "
                  "internally inconsistent with its own growth.",
    },
    {
        "id": "dcf-sustainable-g", "topic": "WACC & DCF", "subtopic": "Consistency check",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 3, slide 16",
        "prompt": "Terminal ROIC 15%, reinvestment rate 30%. What sustainable growth rate "
                  "does that support? Enter a percent.",
        "hint": "g = ROIC × RR.",
        "answer": 4.5, "unit": "%", "tol": 0.1, "answer_label": "Sustainable growth",
        "worked": "0.15 × 0.30 = **4.5%**. Just check it against long-run nominal economic "
                  "growth before using it in perpetuity.",
    },
    {
        "id": "dcf-midyear", "topic": "WACC & DCF", "subtopic": "Discounting",
        "level": "Core", "fmt": "mcq", "source": "Lecture 3, slide 19",
        "prompt": "Switching from end-year to mid-year discounting generally…",
        "choices": ["Lowers present value", "Raises present value",
                    "Has no effect on present value", "Only affects the terminal value"],
        "correct": 1,
        "hint": "Cash is assumed to arrive halfway through each year — sooner.",
        "worked": "**Raises PV** — cash is discounted over a shorter period. At ~10% WACC "
                  "the uplift is roughly 5%. Pick one convention and apply it consistently.",
    },
    {
        "id": "dcf-wacc-g", "topic": "WACC & DCF", "subtopic": "Terminal value",
        "level": "Core", "fmt": "mcq", "source": "Lecture 3, slide 15",
        "prompt": "The Gordon terminal value formula requires that…",
        "choices": ["g > WACC", "WACC > g", "g = WACC", "g = 0"],
        "correct": 1,
        "hint": "Look at the denominator (WACC − g).",
        "worked": "**WACC > g**, or the denominator (WACC − g) goes to zero/negative and "
                  "the formula breaks. Terminal g should also not exceed long-run nominal "
                  "economic growth.",
    },

    # ================================================================
    # MULTIPLES & DEALS (Lecture 4)
    # ================================================================
    {
        "id": "mult-price", "topic": "Multiples & Deals", "subtopic": "Mechanics",
        "level": "Core", "fmt": "numeric", "source": "Lecture 4, slide 10",
        "prompt": "Peers trade at 10x EV/EBITDA. The target has $100M EBITDA, $300M net "
                  "debt, 50M diluted shares. What is the **implied share price**?",
        "hint": "Multiple → EV → subtract net debt → ÷ shares.",
        "answer": 14.0, "unit": "$", "tol": 0.05, "answer_label": "Implied share price",
        "worked": "EV = 10 × 100 = $1,000M. Equity = 1,000 − 300 = $700M. "
                  "Price = 700 / 50 = **$14.00**.",
    },
    {
        "id": "mult-multiple", "topic": "Multiples & Deals", "subtopic": "Mechanics",
        "level": "Core", "fmt": "numeric", "source": "Lecture 4, slide 11",
        "prompt": "A company trades at $20/share, 50M diluted shares, $200M net debt, "
                  "$100M EBITDA. What is its **EV/EBITDA**? Enter a multiple, e.g. 12.",
        "hint": "Price → equity → EV → ÷ EBITDA.",
        "answer": 12.0, "unit": "x", "tol": 0.1, "answer_label": "EV/EBITDA",
        "worked": "Market cap = 20 × 50 = $1,000M. EV = 1,000 + 200 = $1,200M. "
                  "EV/EBITDA = 1,200 / 100 = **12.0x**.",
    },
    {
        "id": "mult-price2", "topic": "Multiples & Deals", "subtopic": "Mechanics",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 4 method",
        "prompt": "Peers trade at 9x EV/EBITDA. Target EBITDA $150M, net debt $400M, 40M "
                  "shares. Implied share price?",
        "hint": "Same chain: EV → equity → per share.",
        "answer": 23.75, "unit": "$", "tol": 0.05, "answer_label": "Implied share price",
        "worked": "EV = 9 × 150 = $1,350M. Equity = 1,350 − 400 = $950M. "
                  "Price = 950 / 40 = **$23.75**.",
    },
    {
        "id": "mult-ev-net", "topic": "Multiples & Deals", "subtopic": "EV pairing",
        "level": "Core", "fmt": "mcq", "source": "Lecture 4, slide 3",
        "prompt": "Which multiple is a **mismatch** you should avoid?",
        "choices": ["EV / EBITDA", "EV / EBIT", "EV / Net Income", "P / E"],
        "correct": 2,
        "hint": "Match the numerator's claim to the denominator's claim.",
        "worked": "**EV / Net Income** pairs an enterprise numerator (debt + equity) with "
                  "an equity-level, after-interest metric. Enterprise numerator → "
                  "pre-interest operating metric; equity numerator → equity metric.",
    },
    {
        "id": "mult-evrev", "topic": "Multiples & Deals", "subtopic": "Choosing multiples",
        "level": "Core", "fmt": "mcq", "source": "Lecture 4, slides 4-5",
        "prompt": "EV/Revenue is *most* useful when…",
        "choices": ["The firm is a mature, profitable bank",
                    "EBITDA is negative or margins differ materially",
                    "You want an equity-level comparison",
                    "Capex intensity is identical across peers"],
        "correct": 1,
        "hint": "Think early-stage or loss-making.",
        "worked": "**When EBITDA is negative or margins differ materially** — e.g. "
                  "early-stage tech with no profits yet. Revenue quality then carries the "
                  "comparison.",
    },
    {
        "id": "mult-implied-ev", "topic": "Multiples & Deals", "subtopic": "Precedents",
        "level": "Core", "fmt": "numeric", "source": "Lecture 4, slide 15",
        "prompt": "A manufacturing business has $120M EBITDA. At the precedent median of "
                  "11.2x EV/EBITDA, what is the **implied Enterprise Value**?",
        "hint": "Implied EV = multiple × metric.",
        "answer": 1344, "unit": "$M", "tol": 2, "answer_label": "Implied EV",
        "worked": "11.2 × 120 = **$1,344M** (≈ $1.34B). The DCF at 10.5x gives $1.26B; a "
                  "12.5x client expectation ($1.50B) needs a premium case.",
    },
    {
        "id": "mult-premium", "topic": "Multiples & Deals", "subtopic": "Control premium",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 4, slide 12",
        "prompt": "A target's unaffected price is $40/share; the offer is $52/share. What "
                  "is the **control premium**? Enter a percent.",
        "hint": "(offer − unaffected) / unaffected.",
        "answer": 30, "unit": "%", "tol": 0.5, "answer_label": "Control premium",
        "worked": "(52 − 40) / 40 = **30%**. Precedent transactions usually embed control "
                  "and synergy value relative to unaffected trading prices — but the size "
                  "varies widely, so don't treat it as a fixed rule.",
    },
    {
        "id": "mult-precedent", "topic": "Multiples & Deals", "subtopic": "Precedents",
        "level": "Core", "fmt": "mcq", "source": "Lecture 4, slides 12-13",
        "prompt": "Relative to unaffected trading prices, precedent-transaction multiples "
                  "typically…",
        "choices": ["Are lower, because deals are distressed",
                    "Include a control/synergy premium",
                    "Are identical to trading comps",
                    "Ignore the buyer type entirely"],
        "correct": 1,
        "hint": "Real deals usually change hands with control.",
        "worked": "They usually **include a control/synergy premium**. But don't treat "
                  "precedents as an automatic ceiling or comps as an automatic floor — "
                  "they're different lenses, and recency matters less than relevance.",
    },
    {
        "id": "mult-synergy", "topic": "Multiples & Deals", "subtopic": "Synergies",
        "level": "Stretch", "fmt": "numeric", "source": "Lecture 4, slide 20",
        "prompt": "After-tax run-rate synergies of $150M/yr, fully realised next year, "
                  "perpetual, no growth, no integration cost, discounted at 8%. What is the "
                  "**total synergy value**?",
        "hint": "A no-growth perpetuity: annual / r.",
        "answer": 1875, "unit": "$M", "tol": 2, "answer_label": "Synergy value",
        "worked": "150 / 0.08 = **$1,875M** ($37.50 per share on 50M shares). In a real "
                  "deal, synergies are ramped, tax-effected, net of integration cost, and "
                  "risk-discounted — don't use annual ÷ WACC as a universal formula.",
    },
    {
        "id": "mult-ceiling", "topic": "Multiples & Deals", "subtopic": "Bidding",
        "level": "Interview-hard", "fmt": "numeric", "source": "Lecture 4, slides 19-21",
        "prompt": "Buy-side. Standalone DCF high is $58/share; full synergy value is $37.50 "
                  "per share. What is the **theoretical bidding ceiling** (pay away all "
                  "synergy)?",
        "hint": "Ceiling = standalone anchor + full synergy per share.",
        "answer": 95.5, "unit": "$", "tol": 0.1, "answer_label": "Theoretical ceiling",
        "worked": "58.00 + 37.50 = **$95.50**. That's the point where you've handed the "
                  "seller every dollar of synergy — a boundary, not a target.",
    },
    {
        "id": "mult-walkaway", "topic": "Multiples & Deals", "subtopic": "Bidding",
        "level": "Interview-hard", "fmt": "numeric", "source": "Lecture 4, slide 21",
        "prompt": "Same deal. If the buyer's discipline rule is to keep **at least half** "
                  "the synergy value, what is the walk-away price? (Standalone anchor $58, "
                  "synergy $37.50/share.)",
        "hint": "Anchor + half the synergy.",
        "answer": 76.75, "unit": "$", "tol": 0.1, "answer_label": "Walk-away price",
        "worked": "58 + (37.50 / 2) = **$76.75**. Below the $95.50 ceiling, and it leaves "
                  "half the synergy for the buyer's own shareholders. An opening bid near "
                  "$60–65 is a defensible 33–44% premium to a $45 trading price.",
    },
    {
        "id": "mult-saas-disc", "topic": "Multiples & Deals", "subtopic": "Judgment",
        "level": "Interview-hard", "fmt": "reveal", "source": "Lecture 4, slides 8-9",
        "prompt": "A SaaS target: 30% growth, 15% EBITDA margin, 85% recurring revenue. "
                  "Peers trade 8–12x EV/Revenue (median 10x), your DCF implies 11.5x, but "
                  "the target itself trades at 7.5x. What do you recommend?",
        "hint": "Don't call it cheap until you've explained the discount.",
        "worked": "**Investigate before concluding.** The 7.5x vs 10x median is a discount "
                  "that needs a reason — test retention/churn, customer concentration, cash "
                  "conversion, stock-based comp and execution risk. Superior growth, "
                  "recurring mix and margins *support* a premium, so if the quality checks "
                  "hold, a selected 10.5–11.5x range may be defensible — a 40–53% uplift in "
                  "implied EV before bridge effects. But lead with the diligence, not the "
                  "conclusion.",
    },
    {
        "id": "mult-football", "topic": "Multiples & Deals", "subtopic": "Triangulation",
        "level": "Core", "fmt": "reveal", "source": "Lecture 4, slides 16-18",
        "prompt": "How do you read a football field where DCF is 42–58, trading comps "
                  "45–52, precedents 51–62, and sum-of-parts 47–59?",
        "hint": "Look for where the ranges cluster, then apply judgment on reliability.",
        "worked": "The methods overlap most around **~$50–55**, which is a useful "
                  "reference. But triangulation isn't averaging — explain *why* methods "
                  "diverge (precedents sit higher because they embed control; comps inherit "
                  "market mood) before landing a range, and weight whichever lens is most "
                  "reliable for *this* situation (sale vs. staying public, deal recency, "
                  "peer cleanliness).",
    },
    {
        "id": "mult-client", "topic": "Multiples & Deals", "subtopic": "Judgment",
        "level": "Interview-hard", "fmt": "reveal", "source": "Lecture 4, slides 14-15",
        "prompt": "Selling a manufacturer ($800M revenue, $120M EBITDA). Eight deals over "
                  "24 months show 9.0–13.5x (median 11.2x); your DCF says 10.5x. The client "
                  "wants 12.5x+ and points to one 15x outlier. Your advice?",
        "hint": "Anchor to the evidence, interrogate the outlier, manage expectations.",
        "worked": "Anchor on the **median 11.2x** and DCF 10.5x: a 12.5x expectation needs "
                  "a premium case. Interrogate the 15x outlier — scarcity, strategic fit, "
                  "unusual growth, competitive auction? If the asset is genuinely premium "
                  "with real buyer tension, 12x+ can be defensible; otherwise guide toward "
                  "the middle of the precedent range. Remember a seller's reserve is a "
                  "*minimum* acceptable price, not a stretch target.",
    },
]


# ------------------------------------------------------------------ helpers
TOPICS = ["Accounting", "FCFF & Drivers", "WACC & DCF", "Multiples & Deals"]
LEVELS = ["Core", "Stretch", "Interview-hard"]
FORMATS = {"reveal": "Concept / walk-through", "numeric": "Numeric", "mcq": "Multiple choice"}


def by_topic(topic=None, level=None, fmt=None):
    out = QUESTIONS
    if topic:
        out = [q for q in out if q["topic"] == topic]
    if level:
        out = [q for q in out if q["level"] == level]
    if fmt:
        out = [q for q in out if q["fmt"] == fmt]
    return out


# ------------------------------------------------------------------ self-test
if __name__ == "__main__":
    ids = [q["id"] for q in QUESTIONS]
    assert len(ids) == len(set(ids)), "duplicate id!"
    for q in QUESTIONS:
        assert q["topic"] in TOPICS, q["id"]
        assert q["level"] in LEVELS, q["id"]
        assert q["fmt"] in FORMATS, q["id"]
        if q["fmt"] == "numeric":
            assert "answer" in q and "tol" in q and "unit" in q, q["id"]
        if q["fmt"] == "mcq":
            assert 0 <= q["correct"] < len(q["choices"]), q["id"]
    n = len(QUESTIONS)
    print(f"{n} questions OK")
    for t in TOPICS:
        c = len(by_topic(topic=t))
        print(f"  {t}: {c}")
    for fmt in FORMATS:
        print(f"  [{fmt}] {len(by_topic(fmt=fmt))}")
