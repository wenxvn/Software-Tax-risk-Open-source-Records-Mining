from datetime import date

import pandas as pd
import pytest

from taxrisk.db import DatabaseManager
from taxrisk.models import (
    EvidenceRecord,
    LineageRecord,
    PolicyRecord,
    RiskRecord,
    SourceRecord,
    validate_rule_template,
)
from taxrisk.reconciliation import reconcile_revenue


def test_source_and_lineage_schema():
    assert SourceRecord(source_id="s1", file_name="a.csv", file_hash="a" * 64, source_type="CSV").source_id == "s1"
    assert LineageRecord(output_field="x", source_file="a.csv", transformation="identity").output_field == "x"


def test_empty_reconciliation_and_missing_columns():
    empty = pd.DataFrame(columns=["period", "revenue"])
    assert reconcile_revenue(empty, empty).empty
    with pytest.raises(ValueError):
        reconcile_revenue(pd.DataFrame(), empty)


def test_amount_and_date_parsing():
    frame = pd.DataFrame({"period": pd.to_datetime(["2026-01-01"]), "revenue": [12.5]})
    assert frame.revenue.sum() == pytest.approx(12.5)
    assert frame.period.iloc[0].date() == date(2026, 1, 1)


def test_duckdb_query():
    with DatabaseManager(":memory:") as db:
        db.register("t", pd.DataFrame({"x": [1, 2]}))
        assert db.query("select sum(x) as total from t").iloc[0]["total"] == 3


def test_rule_schema():
    assert validate_rule_template({"rule_id": "x", "name": "x", "tax_type": "TODO", "status": "TEMPLATE_ONLY", "inputs": [], "formula": "TODO", "threshold": {}, "policy_basis": []})["status"] == "TEMPLATE_ONLY"
    with pytest.raises(ValueError):
        validate_rule_template({"rule_id": "x"})


def test_evidence_policy_and_risk_schema():
    assert EvidenceRecord(evidence_id="e", risk_id="r", evidence_type="raw", source_id="s", location="x", description="d").verified is False
    assert PolicyRecord(policy_id="p", title="t", issuer="国家税务总局", source_url="https://example.gov.cn", status="NEEDS_REVIEW").status == "NEEDS_REVIEW"
    assert RiskRecord(risk_id="r", rule_id="x", tax_type="TODO", business_process="x", status="ANOMALY", anomaly_score=1).status == "ANOMALY"

