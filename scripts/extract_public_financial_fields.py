"""Create a reproducible, public-disclosure-only field dataset for candidate screening."""

from __future__ import annotations

import csv
from pathlib import Path

from taxrisk.disclosures import first_report_page
from taxrisk.public_fields import FIELD_PATTERNS, extract_public_financial_fields
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "sources" / "curated" / "open_data" / "yonyou"
NUMERIC_OUTPUT = ROOT / "outputs" / "tables" / "yonyou_public_financial_fields.csv"
AVAILABILITY_OUTPUT = ROOT / "docs" / "research" / "yonyou_public_field_availability.csv"
YEARS = (2023, 2024)

tracker = install_script_logging(
    "extract_public_financial_fields",
    "python scripts/extract_public_financial_fields.py",
    "PHASE 1",
    ROOT,
    [NUMERIC_OUTPUT.relative_to(ROOT), AVAILABILITY_OUTPUT.relative_to(ROOT)],
)
numeric_rows: list[dict[str, object]] = []
availability_rows: list[dict[str, object]] = []
for year in YEARS:
    source_id = f"PUB-YY-{year}-AR"
    source_text = (REPORT_DIR / f"{year}_annual_report.txt").read_text(encoding="utf-8")
    fields = extract_public_financial_fields(source_text)
    for field, amount in fields.items():
        source_section, pattern = FIELD_PATTERNS[field]
        numeric_rows.append(
            {
                "source_id": source_id,
                "period": str(year),
                "field": field,
                "amount_cny": amount,
                "currency": "CNY",
                "basis": "CONSOLIDATED_PUBLIC_FINANCIAL_STATEMENT",
                "source_file": str((REPORT_DIR / f"{year}_annual_report.txt").relative_to(ROOT)),
                "source_section": source_section,
                "report_page": first_report_page(source_text, source_section),
                "transformation": "regex_current_period_amount",
                "code_reference": "src/taxrisk/public_fields.py",
                "research_boundary": "PUBLIC_DISCLOSURE_ONLY; NOT_TAX_FILING_OR_LEDGER",
            }
        )
        availability_rows.append(
            {
                "source_id": source_id,
                "period": str(year),
                "field": field,
                "available": True,
                "source_section": source_section,
                "report_page": first_report_page(source_text, source_section),
                "status": "PUBLIC_FIELD_ONLY",
                "missing_for_tax_conclusion": "tax_return,invoices,contracts,orders,bank_records,business_explanation",
            }
        )
    tracker.note(f"{source_id}: extracted {len(fields)} public numeric fields")

for output, rows in ((NUMERIC_OUTPUT, numeric_rows), (AVAILABILITY_OUTPUT, availability_rows)):
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
print(f"extracted {len(numeric_rows)} public fields: {NUMERIC_OUTPUT}")
print(f"field availability written: {AVAILABILITY_OUTPUT}")
