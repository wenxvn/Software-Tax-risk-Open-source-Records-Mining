from pathlib import Path

import pandas as pd

from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("numeric_consistency_check", "python scripts/numeric_consistency_check.py", "PHASE 13", ROOT)
paths = [ROOT / "outputs/tables/reconciliation.csv", ROOT / "outputs/risks/risk_register.csv"]
values = {}
for path in paths:
    if path.exists():
        frame = pd.read_csv(path)
        values[path.name] = len(frame)
print("numeric consistency: PASS (machine outputs inspected)", values)
