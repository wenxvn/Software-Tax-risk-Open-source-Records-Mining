from pathlib import Path

import pandas as pd

from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
install_script_logging("build_data_dictionary", "python scripts/build_data_dictionary.py", "PHASE 3", ROOT, ["data/dictionaries/data_dictionary.csv"])
rows = []
for path in sorted((ROOT / "data/raw").rglob("*")):
    if path.suffix.lower() == ".csv":
        frame = pd.read_csv(path, nrows=0)
        rows.extend({"file": str(path.relative_to(ROOT)), "field": c, "dtype": str(frame[c].dtype)} for c in frame.columns)
out = ROOT / "data/dictionaries/data_dictionary.csv"
out.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows, columns=["file", "field", "dtype"]).to_csv(out, index=False)
print(f"dictionary written: {out}")
