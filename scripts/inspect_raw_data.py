from pathlib import Path

from taxrisk.integrity import build_manifest
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT / "data/raw"
manifest = ROOT / "sources/manifest.csv"
install_script_logging("inspect_raw_data", "python scripts/inspect_raw_data.py", "PHASE 2", ROOT, [str(manifest)])
files = [p for p in raw.rglob("*") if p.is_file() and p.name != ".gitkeep"]
print(f"raw files: {len(files)}")
for path in files:
    print(path.relative_to(ROOT), path.stat().st_size, "bytes")
build_manifest(raw, manifest)
print(f"manifest written: {manifest}")
