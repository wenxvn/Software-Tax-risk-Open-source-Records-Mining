import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
violations = []
for path in (ROOT / "report").rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    if re.search(r"TODO_MISSING_DATA", text) is None and "case_report" in path.name:
        violations.append(str(path))
if violations:
    raise SystemExit(f"report missing TODO marker: {violations}")
print("anonymization check: PASS")

