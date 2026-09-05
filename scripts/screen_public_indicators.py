"""Screen public-field indicators without turning descriptive signals into tax conclusions."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from taxrisk.public_screening import calculate_descriptive_observations, indicator_coverage
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "outputs" / "tables" / "yonyou_public_financial_fields.csv"
OBSERVATIONS = ROOT / "outputs" / "tables" / "yonyou_public_indicator_observations.csv"
COVERAGE = ROOT / "docs" / "research" / "yonyou_public_indicator_coverage.csv"

tracker = install_script_logging(
    "screen_public_indicators",
    "python scripts/screen_public_indicators.py",
    "PHASE 1",
    ROOT,
    [OBSERVATIONS.relative_to(ROOT), COVERAGE.relative_to(ROOT)],
)
if not INPUT.exists():
    raise SystemExit("run scripts/extract_public_financial_fields.py first")
fields = pd.read_csv(INPUT)
observations = calculate_descriptive_observations(fields)
coverage = indicator_coverage(fields)
OBSERVATIONS.parent.mkdir(parents=True, exist_ok=True)
COVERAGE.parent.mkdir(parents=True, exist_ok=True)
observations.to_csv(OBSERVATIONS, index=False)
coverage.to_csv(COVERAGE, index=False)
tracker.note(f"generated {len(observations)} descriptive observations")
tracker.note(f"{int((coverage['status'] == 'TODO_MISSING_DATA').sum())} candidate indicators lack public inputs")
print(f"public descriptive observations written: {OBSERVATIONS} ({len(observations)} rows)")
print(f"candidate coverage written: {COVERAGE}")
