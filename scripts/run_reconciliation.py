from pathlib import Path

import pandas as pd

from taxrisk.reconciliation import reconcile_revenue

ROOT = Path(__file__).resolve().parents[1]
fixture = ROOT / "data/fixtures/synthetic_revenue"
accounting = pd.read_csv(fixture / "accounting_revenue.csv")
filing = pd.read_csv(fixture / "filing_revenue.csv")
result = reconcile_revenue(accounting, filing)
out = ROOT / "outputs/tables/reconciliation.csv"
out.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(out, index=False)
print(result.to_string(index=False))
print(f"written: {out}")

