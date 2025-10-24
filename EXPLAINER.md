# EBAN-STACK — Explainer & Learning Plan

This file summarizes everything created in the EBAN-STACK scaffold, why it matters for improving your technical skills, and an actionable learning plan you can follow.

Location: `C:\Users\digitalscorpyun\upgrade_tech_stak_game`

---

## Quick project snapshot

What you have (high-level):

- A small, runnable Python package under `src/eban_stack` that contains:
  - `risk_checks.py` — overdraft-detection heuristics (typed, documented)
  - `explain.py` — human-readable explanations, summary, recommendations
  - `io.py` — CSV I/O, validation, helper to generate sample data
- A minimal Streamlit demo at `src/app/streamlit_app.py` that:
  - accepts CSV uploads, runs analysis, attaches explanations per row, shows metrics, and allows download/save
- Tests and sample data:
  - `tests/test_risk_checks.py` — unit tests for logic
  - `tests/sample_budget.csv` — synthetic dataset (20+ rows) including overdrafts
  - `tests/conftest.py` — puts `src/` on `sys.path` for tests
- Policy and training artifacts:
  - `policy/policy_memo_template.md`, `policy/model_card_template.md`, `policy/risk_register.csv`
  - `training/micro_video_script_template.md`, `training/user_tooltips.md`
- Developer ergonomics:
  - `.vscode/tasks.json` — venv creation, dependencies, run app, run tests, composite `setup: all`
  - `requirements.txt`, `pyproject.toml`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`

All tests were run in a virtual environment and succeeded: `2 passed`.

---

## Why this setup will improve your technical know-how

This scaffold is intentionally small but touches key areas used by professional engineers, data scientists, and cloud engineers. Working through it helps you practice these skills:

- Clean Python engineering: type hints, dataclasses, docstrings, small functions with clear inputs/outputs.
- Data engineering basics: CSV I/O, validation, handling numeric edge cases, basic ETL patterns.
- Testing and reproducibility: writing unit tests with pytest, deterministic synthetic datasets, `conftest.py` patterns.
- Interpretability & UX: translating logic into human-facing explanations in `explain.py` and surfacing them in a UI.
- Productization: building a lightweight Streamlit app to make models/heuristics usable and testable by non-programmers.
- Policy & ethics practice: linking technical behaviour to policy artifacts (memo, model card, risk register).
- Developer tooling: virtual environments, dependency management, VS Code tasks, and preparing the codebase for CI and linters.

These are all practical, high-impact skills that scale to larger projects.

---

## Short actionable exercises (ordered, with acceptance criteria)

1) Environment + tests (5–20 minutes)
   - What: Create a venv, install deps, run tests.
   - Commands (PowerShell):
     ```powershell
     cd C:\Users\digitalscorpyun\upgrade_tech_stak_game
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     .\.venv\Scripts\pytest -q
     ```
   - Acceptance: pytest shows `2 passed`.

2) Run the Streamlit demo (10–30 minutes)
   - What: Start the app and upload `tests/sample_budget.csv`.
   - Command:
     ```powershell
     .\.venv\Scripts\Activate.ps1
     streamlit run src\app\streamlit_app.py
     ```
   - Acceptance: The UI loads, displays rows, shows overdraft count, and shows per-row explanations.

3) TDD: Add a “large withdrawal” rule (30–90 minutes)
   - What: Add a rule in `risk_checks.py` to flag any debit where `abs(amount)` > 40% of balance.
   - Steps: write a failing test in `tests/`; implement rule; ensure tests pass.
   - Acceptance: New test passes and code includes docstring and type hints.

4) Improve explanations (15–45 minutes)
   - What: Enhance `explain_row` to include keyword-based context from `description` (e.g., "Rent", "Salary").
   - Acceptance: App shows more descriptive `explain_text` for rows with those keywords.

5) Add static analysis and pre-commit (1–3 hours)
   - What: Add `black`, `flake8`, `mypy`, and a `pre-commit` config. Run and fix issues.
   - Acceptance: `pre-commit run --all-files` runs (and either passes or autofixes formatting).

6) Add CI (1–3 hours)
   - What: Add a GitHub Actions workflow to run tests on push.
   - Acceptance: Workflow runs and passes on the repository (or you see a successful run in Actions).

---

## Suggested learning roadmap (4 weeks)

Week 1 — Fundamentals
- Complete exercises 1–3. Focus: TDD and small API design.

Week 2 — Quality & tooling
- Add linters and pre-commit. Start using VS Code tasks routinely. Add type checking where missing.

Week 3 — Policy & fairness
- Implement a fairness slice (add `segment` to sample data), compute group metrics, and write a short policy memo.

Week 4 — CI/CD and packaging
- Add GitHub Actions, create a `setup.cfg`/`pyproject` packaging flow, and draft a release on GitHub.

---

## Next steps I can take for you (pick one)
- Run the Streamlit app now and capture runtime logs / screenshots.
- Implement exercise 3 (large-withdrawal rule) end-to-end with tests.
- Add pre-commit hooks and a basic `pyproject.toml` configuration for `black` and `mypy`.
- Draft a 2-page policy memo in `policy/policy_memo_template.md` with owners/KPIs.

Tell me which and I will implement it directly.

---

## Where to open this file

Open with your editor (VS Code) or any text viewer:
- Path: `C:\Users\digitalscorpyun\upgrade_tech_stak_game\EXPLAINER.md`

Thank you — tell me which next step above to do and I will proceed.
