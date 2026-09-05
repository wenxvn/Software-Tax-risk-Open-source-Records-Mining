"""Small, deterministic helpers for publicly disclosed source documents."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def load_report_index(path: str | Path) -> list[dict[str, Any]]:
    """Load the issuer's report index response, rejecting an unexpected shape."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    content = payload.get("data", {}).get("content", [])
    if not isinstance(content, list):
        raise ValueError("report index does not contain data.content list")
    return content


def annual_report_url(records: list[dict[str, Any]], year: int) -> str:
    """Return the single issuer-hosted PDF URL for a named annual report year."""
    expected_title = f"用友网络{year}年年度报告"
    matches = [record for record in records if record.get("title") == expected_title]
    if len(matches) != 1:
        raise ValueError(f"expected one report-index entry for {expected_title}, got {len(matches)}")
    files = matches[0].get("files", [])
    if len(files) != 1 or not isinstance(files[0].get("furl"), str):
        raise ValueError(f"expected one PDF URL for {expected_title}")
    return files[0]["furl"]


def required_text_check(text: str, year: int) -> dict[str, bool]:
    """Check document identity and the public fields required for candidate screening."""
    checks = {
        "security_code_600588": "600588" in text,
        "report_year": f"{year} 年年度报告" in text,
        "standard_unqualified_audit_opinion": "标准无保留意见" in text,
        "consolidated_balance_sheet": "合并资产负债表" in text,
        "consolidated_income_statement": "合并利润表" in text,
        "consolidated_cash_flow_statement": "合并现金流量表" in text,
        "accounts_receivable": "应收账款" in text,
        "contract_liabilities": "合同负债" in text,
        "research_and_development_expense": "研发费用" in text,
        "income_tax_expense": "所得税费用" in text,
        "government_grants": "政府补助" in text,
        "related_party_transactions": "关联交易" in text,
    }
    return checks


def first_report_page(text: str, term: str) -> int | None:
    """Find the printed report page nearest the first occurrence of ``term``."""
    position = text.find(term)
    if position < 0:
        return None
    prefix = text[:position]
    pages = re.findall(r"\n\s*(\d+)\s*/\s*\d+\s*\n", prefix)
    return int(pages[-1]) if pages else None
