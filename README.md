# EBAN-STACK
Bridging tech, policy, and community with a hands-on budgeting risk demo + policy pack.

## Quickstart (Windows)
```powershell
cd C:\Users\digitalscorpyun\upgrade_tech_stak_game
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# run tests
pytest -q
# run app
streamlit run src\app\streamlit_app.py
```

## What’s here

* `src/eban_stack`: simple risk logic + explainers
* `src/app/streamlit_app.py`: demo UI
* `policy/`: memo + model card templates + risk register
* `training/`: micro-video and tooltip content
* `notebooks/`: start your EDA here

