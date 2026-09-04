"""Raw-data hashing and manifest checks."""
import hashlib
from pathlib import Path

import pandas as pd


def sha256_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(raw_dir: str | Path, manifest_path: str | Path) -> pd.DataFrame:
    root = Path(raw_dir)
    rows = [
        {"file_name": str(p.relative_to(root)), "file_hash": sha256_file(p)}
        for p in sorted(root.rglob("*"))
        if p.is_file() and p.name != ".gitkeep"
    ]
    frame = pd.DataFrame(rows, columns=["file_name", "file_hash"])
    Path(manifest_path).parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(manifest_path, index=False)
    return frame


def verify_manifest(raw_dir: str | Path, manifest_path: str | Path) -> pd.DataFrame:
    expected = pd.read_csv(manifest_path) if Path(manifest_path).exists() else pd.DataFrame(columns=["file_name", "file_hash"])
    root = Path(raw_dir)
    actual = pd.DataFrame(
        [
            {"file_name": str(p.relative_to(root)), "file_hash": sha256_file(p)}
            for p in sorted(root.rglob("*"))
            if p.is_file() and p.name != ".gitkeep"
        ],
        columns=["file_name", "file_hash"],
    )
    merged = expected.merge(actual, on="file_name", how="outer", suffixes=("_expected", "_actual"), indicator=True)
    merged["unchanged"] = (merged["_merge"] == "both") & (merged["file_hash_expected"] == merged["file_hash_actual"])
    return merged
