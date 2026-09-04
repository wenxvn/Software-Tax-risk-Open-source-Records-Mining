from pathlib import Path

import pandas as pd

from taxrisk.models import RiskRecord
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("run_risk_scan", "python scripts/run_risk_scan.py", "PHASE 8", ROOT, ["outputs/risks/risk_register.csv"])
recon = ROOT / "outputs/tables/reconciliation.csv"
if not recon.exists():
    raise SystemExit("run_reconciliation.py first")
frame = pd.read_csv(recon)
rows = []
for i, row in frame.iterrows():
    status = "OBSERVATION" if row["status"] == "CLEARED" else "ANOMALY"
    record = RiskRecord(risk_id=f"SMOKE-{i+1:03d}", rule_id="TEMPLATE_RECON_001", tax_type="TODO", business_process="SYNTHETIC_TEST_DATA_ONLY", status=status, anomaly_score=0.0 if status == "OBSERVATION" else 1.0, amount=float(abs(row["difference"])), reviewer_status="NOT_FOR_CASE")
    rows.append(record.model_dump())
out = ROOT / "outputs/risks/risk_register.csv"
out.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out, index=False)
print(f"risk scan written: {out} (synthetic only; no tax conclusion)")
