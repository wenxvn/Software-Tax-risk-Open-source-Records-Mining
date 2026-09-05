"""Archive official policy candidate pages and register their verified metadata."""

from __future__ import annotations

import csv
import hashlib
import urllib.request
from datetime import date
from pathlib import Path

from taxrisk.policy_sources import POLICY_CANDIDATES, html_to_text
from taxrisk.workflow import install_script_logging

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "sources" / "policies" / "raw"
TEXT_DIR = ROOT / "sources" / "policies" / "text"
INDEX = ROOT / "sources" / "policies" / "index.csv"
SUMMARY = ROOT / "docs" / "research" / "policy_candidate_summary.csv"
INDEX_FIELDS = [
    "policy_id",
    "title",
    "document_number",
    "issuer",
    "publish_date",
    "effective_date",
    "expiry_date",
    "amendment_status",
    "article",
    "applicable_taxpayer",
    "applicable_business",
    "source_url",
    "verification_date",
    "case_period_applicable",
    "notes",
    "status",
]


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.read()


tracker = install_script_logging(
    "collect_policy_candidates",
    "python scripts/collect_policy_candidates.py",
    "PHASE 1",
    ROOT,
    [INDEX.relative_to(ROOT), SUMMARY.relative_to(ROOT)],
)
RAW_DIR.mkdir(parents=True, exist_ok=True)
TEXT_DIR.mkdir(parents=True, exist_ok=True)
summary_rows: list[dict[str, object]] = []
index_rows: list[dict[str, str]] = []
for candidate in POLICY_CANDIDATES:
    policy_id = candidate["policy_id"]
    raw = fetch(candidate["source_url"])
    raw_path = RAW_DIR / f"{policy_id}.html"
    text_path = TEXT_DIR / f"{policy_id}.txt"
    raw_path.write_bytes(raw)
    text_path.write_text(html_to_text(raw.decode("utf-8", errors="replace")), encoding="utf-8")
    file_hash = hashlib.sha256(raw).hexdigest()
    index_row = {field: str(candidate.get(field, "")) for field in INDEX_FIELDS}
    index_row["verification_date"] = date.today().isoformat()
    index_rows.append(index_row)
    summary_rows.append(
        {
            "policy_id": policy_id,
            "tax_type": "增值税" if "VAT" in policy_id else ("印花税" if "STAMP" in policy_id else "企业所得税"),
            "status": candidate["status"],
            "case_period_applicable": candidate["case_period_applicable"],
            "official_source": candidate["source_url"],
            "raw_file": str(raw_path.relative_to(ROOT)),
            "raw_sha256": file_hash,
            "text_file": str(text_path.relative_to(ROOT)),
            "evidence_boundary": candidate["notes"],
        }
    )
    tracker.note(f"{policy_id}: {candidate['status']}")

with INDEX.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=INDEX_FIELDS)
    writer.writeheader()
    writer.writerows(index_rows)
SUMMARY.parent.mkdir(parents=True, exist_ok=True)
with SUMMARY.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0]))
    writer.writeheader()
    writer.writerows(summary_rows)
print(f"registered {len(index_rows)} official policy candidates: {INDEX}")
