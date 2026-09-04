from pathlib import Path

import pandas as pd

from taxrisk.reconciliation import reconcile_revenue
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("run_reconciliation", "python scripts/run_reconciliation.py", "PHASE 7", ROOT, ["outputs/tables/reconciliation.csv"])
fixture = ROOT / "data/fixtures/synthetic_revenue"
accounting = pd.read_csv(fixture / "accounting_revenue.csv")
filing = pd.read_csv(fixture / "filing_revenue.csv")
result = reconcile_revenue(accounting, filing)
out = ROOT / "outputs/tables/reconciliation.csv"
out.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(out, index=False)
print(result.to_string(index=False))
print(f"written: {out}")
