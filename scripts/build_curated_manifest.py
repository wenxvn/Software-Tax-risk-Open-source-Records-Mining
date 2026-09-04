"""Hash the curated research pack so copied materials remain auditable."""
from datetime import date
from pathlib import Path

import pandas as pd

from taxrisk.integrity import sha256_file
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
CURATED = ROOT / "sources/curated"
install_script_logging("build_curated_manifest", "python scripts/build_curated_manifest.py", "PHASE 1", ROOT, ["sources/curated/manifest.csv"])
rows = []
for path in sorted(CURATED.rglob("*")):
    if path.is_file() and path.name != "manifest.csv":
        rows.append(
            {
                "relative_path": str(path.relative_to(ROOT)),
                "sha256": sha256_file(path),
                "collected_date": date.today().isoformat(),
                "source": "copied from 资料汇总 or downloaded from official URL",
                "status": "REFERENCE_ONLY",
            }
        )
out = CURATED / "manifest.csv"
pd.DataFrame(rows, columns=["relative_path", "sha256", "collected_date", "source", "status"]).to_csv(out, index=False)
print(f"curated manifest written: {out} ({len(rows)} files)")
