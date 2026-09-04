from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "sources/policies/index.csv"
frame = pd.read_csv(path)
print(f"policy records: {len(frame)}")
print("POLICY_UNVERIFIED" if frame.empty else "Review each policy status and case_period_applicable")

