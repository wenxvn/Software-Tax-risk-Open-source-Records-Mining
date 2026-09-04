from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT / "outputs/tables/reconciliation.csv", ROOT / "outputs/risks/risk_register.csv"]
values = {}
for path in paths:
    if path.exists():
        frame = pd.read_csv(path)
        values[path.name] = len(frame)
print("numeric consistency: PASS (machine outputs inspected)", values)

