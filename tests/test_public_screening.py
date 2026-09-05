import pandas as pd
import pytest

from taxrisk.public_screening import calculate_descriptive_observations, indicator_coverage


def test_public_observations_are_descriptive_without_thresholds():
    fields = pd.DataFrame(
        [
            {"period": 2023, "field": "operating_revenue", "amount_cny": 100, "source_id": "s23"},
            {"period": 2023, "field": "cash_received_from_sales", "amount_cny": 110, "source_id": "s23"},
            {"period": 2024, "field": "operating_revenue", "amount_cny": 200, "source_id": "s24"},
            {"period": 2024, "field": "cash_received_from_sales", "amount_cny": 180, "source_id": "s24"},
        ]
    )
    observations = calculate_descriptive_observations(fields)
    cash = observations[observations["indicator_id"] == "PUB-IND-01"]
    assert cash["value"].tolist() == [1.1, 0.9]
    assert cash.iloc[1]["change"] == pytest.approx(-0.2)
    assert set(cash["status"]) == {"OBSERVATION"}
    assert set(cash["threshold_basis"]) == {"NONE_DESCRIPTIVE_LONGITUDINAL_COMPARISON_ONLY"}


def test_coverage_marks_missing_contract_evidence_as_missing_data():
    fields = pd.DataFrame(
        [{"period": 2024, "field": "operating_revenue", "amount_cny": 100, "source_id": "s24"}]
    )
    coverage = indicator_coverage(fields)
    stamp = coverage[coverage["indicator_id"] == "PUB-IND-11"].iloc[0]
    assert stamp["status"] == "TODO_MISSING_DATA"
    assert stamp["conclusion_ceiling"] == "NO_CONCLUSION"
