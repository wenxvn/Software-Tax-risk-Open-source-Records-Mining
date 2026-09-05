"""Extract a deliberately narrow set of financial-statement fields from public reports."""

import re

FIELD_PATTERNS = {
    "operating_revenue": ("合并利润表", r"一、营业总收入\s+(-?[\d,]+)"),
    "operating_cost": ("合并利润表", r"其中：营业成本\s+(?:七、61\s+)?(-?[\d,]+)"),
    "taxes_and_surcharges": ("合并利润表", r"税金及附加\s+(?:七、62\s+)?(-?[\d,]+)"),
    "research_and_development_expense": ("合并利润表", r"研发费用\s+(?:七、65\s+)?(-?[\d,]+)"),
    "income_tax_expense": ("合并利润表", r"减：所得税费用\s+(?:七、76\s+)?(-?[\d,]+)"),
    "accounts_receivable": ("合并资产负债表", r"应收账款\s+(?:七、5\s+)?(-?[\d,]+)"),
    "contract_assets": ("合并资产负债表", r"合同资产\s+(?:七、6\s+)?(-?[\d,]+)"),
    "contract_liabilities": ("合并资产负债表", r"合同负债\s+(?:七、38\s+)?(-?[\d,]+)"),
    "taxes_payable": ("合并资产负债表", r"应交税费\s+(?:七、40\s+)?(-?[\d,]+)"),
    "cash_received_from_sales": ("合并现金流量表", r"销售商品、提供劳务收到的\s*现金\s+(-?[\d,]+)"),
    "taxes_paid": ("合并现金流量表", r"支付的各项税费\s+(-?[\d,]+)"),
    "government_grants_recognized_in_profit": (
        "3、 计入当期损益的政府补助",
        r"类型\s+本期发生额\s+上期发生额.*?合计\s+(-?[\d,]+)",
    ),
}


def statement_window(text: str, start: str) -> str:
    """Return the relevant public-report section, ending at the next major statement."""
    start_at = text.find(start)
    if start_at < 0:
        raise ValueError(f"missing source section: {start}")
    section = text[start_at:]
    next_heading = re.search(r"\n(?:合并|母公司)(?:资产负债表|利润表|现金流量表)\s*\n", section[1:])
    return section[: next_heading.start() + 1] if next_heading else section


def extract_first_year_amount(text: str, source_section: str, pattern: str) -> int:
    """Extract the current-period amount from a named report section in yuan."""
    match = re.search(pattern, statement_window(text, source_section), flags=re.DOTALL)
    if not match:
        raise ValueError(f"unable to extract amount with pattern: {pattern}")
    return int(match.group(1).replace(",", ""))


def extract_public_financial_fields(text: str) -> dict[str, int]:
    return {
        field: extract_first_year_amount(text, source_section, pattern)
        for field, (source_section, pattern) in FIELD_PATTERNS.items()
    }
