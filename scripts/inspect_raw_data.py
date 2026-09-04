from pathlib import Path

from taxrisk.integrity import build_manifest

ROOT = Path(__file__).resolve().parents[1]
raw = ROOT / "data/raw"
manifest = ROOT / "sources/manifest.csv"
files = [p for p in raw.rglob("*") if p.is_file() and p.name != ".gitkeep"]
print(f"raw files: {len(files)}")
for path in files:
    print(path.relative_to(ROOT), path.stat().st_size, "bytes")
build_manifest(raw, manifest)
print(f"manifest written: {manifest}")
