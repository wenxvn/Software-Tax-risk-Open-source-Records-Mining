from pathlib import Path

from taxrisk.integrity import verify_manifest

ROOT = Path(__file__).resolve().parents[1]
result = verify_manifest(ROOT / "data/raw", ROOT / "sources/manifest.csv")
if not result.empty and not result["unchanged"].all():
    print(result.to_string(index=False))
    raise SystemExit("raw data changed or manifest is incomplete")
print("raw manifest check: PASS (no raw files or unchanged files)")

