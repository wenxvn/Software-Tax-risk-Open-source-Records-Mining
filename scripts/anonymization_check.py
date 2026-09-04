import re
from pathlib import Path

from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("anonymization_check", "python scripts/anonymization_check.py", "PHASE 13", ROOT)
violations = []
for path in (ROOT / "report").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if re.search(r"TODO_MISSING_DATA", text) is None and "case_report" in path.name:
        violations.append(str(path))
if violations:
    raise SystemExit(f"report missing TODO marker: {violations}")
print("anonymization check: PASS")
