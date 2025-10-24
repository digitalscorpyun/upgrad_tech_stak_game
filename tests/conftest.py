import sys
from pathlib import Path

# Ensure project src/ is on sys.path so imports like `eban_stack` work during tests
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
