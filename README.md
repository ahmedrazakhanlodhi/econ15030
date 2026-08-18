# ECON 15030 — Interview Prep

An interactive study app for the TA sessions of **Basics of Corporate, Banking &
Investment Finance** (University of Chicago, September Term).
Prepared by **Ahmed Raza Khan Lodhi**.

It bundles four things students can use on their own:

1. **Practice questions** — 54 interview-style problems in the
   concept → question → worked-answer format from the sessions, with
   Study / Quiz / Flashcard modes and automatic grading of numeric answers.
2. **Calculators** — FCFF (unlevered NOPAT route), a 5-year driver forecast,
   WACC / CAPM / beta (with Hamada lever/relever), a full DCF with a live
   sensitivity grid, multiples and the EV→Equity bridge, and synergy / bidding.
3. **Lecture slides** — all four decks, browsable in-app.
4. **Thoughtworks capstone** — the Apax take-private, interactive: deteriorate
   the forecast and watch the DCF collapse from the 2023 book range to the 2024
   book range and the eventual close.

Everything numeric — every calculator **and** every graded answer — calls one
shared engine (`lib/finance.py`), so there is a single definition of FCFF, one
DCF assembly, and a sensitivity table that recomputes terminal FCFF for each
growth case. The tool cannot contradict the decks or itself.

---

## Run it locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the URL Streamlit prints (usually http://localhost:8501).

## Deploy on Streamlit Community Cloud (free)

1. Create a **GitHub repo** and push this whole folder to it:
   ```bash
   git init
   git add .
   git commit -m "ECON 15030 interview prep app"
   git branch -M main
   git remote add origin https://github.com/<you>/<repo>.git
   git push -u origin main
   ```
2. Go to **https://share.streamlit.io**, sign in with GitHub, and click
   **Create app → Deploy a public app from GitHub**.
3. Point it at your repo, branch `main`, and **main file path** `app.py`.
4. Click **Deploy**. You'll get a shareable `*.streamlit.app` URL to send
   students. Every `git push` redeploys automatically.

No secrets or API keys are needed.

---

## Project layout

```
app.py                 entry point + sidebar navigation
requirements.txt
.streamlit/config.toml  UChicago-maroon theme
lib/finance.py          canonical finance engine (single source of truth)
data/questions.py       the 54-question bank
sections/
  home.py               overview
  practice.py           Study / Quiz / Flashcards + grading
  calculators.py        7 calculator tabs
  slides.py             deck image viewer
  case.py               Thoughtworks capstone
assets/slides/          rendered slide images (lecture1..4)
```

## Extending it

- **Add practice questions** — append a dict to `QUESTIONS` in
  `data/questions.py`. Use `fmt="reveal"` (concept walk-through),
  `"numeric"` (auto-graded, needs `answer`/`unit`/`tol`/`answer_label`), or
  `"mcq"` (needs `choices`/`correct`). Run `python data/questions.py` to
  validate; numeric answers should be checked against `lib/finance.py`.
- **Update the slides** — re-render the decks to
  `assets/slides/lectureN/slide-NN.jpg` (any tool that exports PPTX pages to
  images works) and the viewer picks them up automatically.
- **Session 5 / real Lazard pages** — `sections/case.py` has a hook at the
  bottom. The driver model there is an **illustrative** reconstruction that
  reproduces the direction and rough magnitude of the two published book
  ranges — it is not the bank's internal model. Swap in the finalised Session-5
  figures, and (rights permitting) add the real football-field / share-price /
  analysis-at-various-prices pages as a thin teaching wrapper. If the deployed
  URL is public, keep confidential bank material out of the repo.

## A note on the numbers

The engine reproduces every worked figure in the four decks exactly (NOPAT 60,
FCFF 8, after-tax-interest wedge 6, unlevered/relevered beta 0.97/1.26,
WACC 9.0% / 9.12%, terminal value 2,575 / 2,365, DCF EV 1,782 and $29.63/share,
EV→Equity bridge 2,075, multiples 14.0x / 12.0x, synergy 1,875 and $37.50).
FCFF is always built the unlevered NOPAT way, so the FCFF = 8 vs FCFF = 2
confusion cannot reappear.
