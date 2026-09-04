from pathlib import Path

import pandas as pd
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("audit_evidence", "python scripts/audit_evidence.py", "PHASE 10", ROOT, ["outputs/evidence/evidence_audit.csv"])
risks = pd.read_csv(ROOT / "outputs/risks/risk_register.csv") if (ROOT / "outputs/risks/risk_register.csv").exists() else pd.DataFrame()
out = ROOT / "outputs/evidence/evidence_audit.csv"
out.parent.mkdir(parents=True, exist_ok=True)
if risks.empty:
    audit = pd.DataFrame(columns=["risk_id", "evidence_completeness", "missing_evidence", "conflicting_evidence", "result"])
else:
    audit = pd.DataFrame({"risk_id": risks["risk_id"], "evidence_completeness": 0.0, "missing_evidence": "TODO_MISSING_DATA", "conflicting_evidence": "", "result": "NOT_READY"})
audit.to_csv(out, index=False)
print(f"evidence audit written: {out}")
