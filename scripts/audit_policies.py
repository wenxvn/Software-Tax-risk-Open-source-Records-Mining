from pathlib import Path

import pandas as pd
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("audit_policies", "python scripts/audit_policies.py", "PHASE 5", ROOT)
path = ROOT / "sources/policies/index.csv"
frame = pd.read_csv(path)
print(f"policy records: {len(frame)}")
print("POLICY_UNVERIFIED" if frame.empty else "Review each policy status and case_period_applicable")
