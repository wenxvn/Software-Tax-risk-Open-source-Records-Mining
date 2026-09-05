import json
from pathlib import Path

import pytest

from taxrisk.disclosures import (
    annual_report_url,
    first_report_page,
    load_report_index,
    required_text_check,
)


def test_report_index_and_annual_url(tmp_path: Path):
    index = tmp_path / "report_index.json"
    index.write_text(
        json.dumps(
            {"data": {"content": [{"title": "用友网络2024年年度报告", "files": [{"furl": "https://issuer.example/2024.pdf"}]}]}},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    assert annual_report_url(load_report_index(index), 2024) == "https://issuer.example/2024.pdf"
    with pytest.raises(ValueError, match="expected one report-index entry"):
        annual_report_url(load_report_index(index), 2023)


def test_required_text_check_and_report_page():
    text = "\n 12 / 100 \n600588\n2024 年年度报告\n标准无保留意见\n合并资产负债表\n合并利润表\n合并现金流量表\n应收账款\n合同负债\n研发费用\n所得税费用\n政府补助\n关联交易"
    assert all(required_text_check(text, 2024).values())
    assert first_report_page(text, "合同负债") == 12
    assert first_report_page(text, "不存在") is None
