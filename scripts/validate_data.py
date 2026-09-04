from pathlib import Path

from taxrisk.integrity import verify_manifest
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("validate_data", "python scripts/validate_data.py", "PHASE 2", ROOT)
result = verify_manifest(ROOT / "data/raw", ROOT / "sources/manifest.csv")
if not result.empty and not result["unchanged"].all():
    print(result.to_string(index=False))
    raise SystemExit("raw data changed or manifest is incomplete")
print("raw manifest check: PASS (no raw files or unchanged files)")
