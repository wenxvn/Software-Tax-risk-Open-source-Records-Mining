"""Verify locally archived issuer annual reports against the issuer's indexed PDFs."""

from __future__ import annotations

import csv
import hashlib
import urllib.request
from datetime import date
from pathlib import Path

from pypdf import PdfReader

from taxrisk.disclosures import annual_report_url, load_report_index, required_text_check
from taxrisk.integrity import sha256_file
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "sources" / "curated" / "open_data" / "yonyou"
OUTPUT = ROOT / "docs" / "research" / "yonyou_annual_report_verification.csv"
YEARS = (2023, 2024)


def remote_sha256(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    digest = hashlib.sha256()
    with urllib.request.urlopen(request, timeout=90) as response:
        while block := response.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


tracker = install_script_logging(
    "verify_public_disclosures",
    "python scripts/verify_public_disclosures.py",
    "PHASE 1",
    ROOT,
    [OUTPUT.relative_to(ROOT)],
)
records = load_report_index(REPORT_DIR / "report_index.json")
rows: list[dict[str, object]] = []
for year in YEARS:
    pdf_path = REPORT_DIR / f"{year}_annual_report.pdf"
    text_path = REPORT_DIR / f"{year}_annual_report.txt"
    source_url = annual_report_url(records, year)
    text = text_path.read_text(encoding="utf-8")
    checks = required_text_check(text, year)
    local_hash = sha256_file(pdf_path)
    downloaded_hash = remote_sha256(source_url)
    row = {
        "source_id": f"PUB-YY-{year}-AR",
        "issuer": "用友网络科技股份有限公司",
        "security_code": "600588",
        "report_period": f"{year}-01-01/{year}-12-31",
        "source_url": source_url,
        "local_pdf": str(pdf_path.relative_to(ROOT)),
        "local_sha256": local_hash,
        "remote_sha256": downloaded_hash,
        "hash_match": local_hash == downloaded_hash,
        "pdf_pages": len(PdfReader(str(pdf_path)).pages),
        "text_extract": str(text_path.relative_to(ROOT)),
        "identity_and_screening_checks_passed": all(checks.values()),
        "screening_check_count": sum(checks.values()),
        "screening_check_total": len(checks),
        "collection_date": date.today().isoformat(),
        "research_boundary": "PUBLIC_DISCLOSURE_ONLY; NOT_INTERNAL_BOOKS_OR_TAX_FILINGS",
        "verification_status": "VERIFIED" if local_hash == downloaded_hash and all(checks.values()) else "FAILED",
    }
    rows.append(row)
    tracker.note(f"{row['source_id']}: {row['verification_status']}")

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

if not all(row["verification_status"] == "VERIFIED" for row in rows):
    raise SystemExit("public disclosure verification failed")
print(f"verified {len(rows)} issuer annual reports: {OUTPUT}")
