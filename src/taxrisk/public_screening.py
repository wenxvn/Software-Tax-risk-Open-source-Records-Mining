"""Descriptive-only indicators calculated from the verified public-field dataset."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class PublicIndicator:
    indicator_id: str
    name: str
    candidate_tax_type: str
    numerator: str | None
    denominator: str | None
    policy_ids: tuple[str, ...]
    evidence_required: str
    policy_state: str = "POLICY_UNVERIFIED"


INDICATORS = (
    PublicIndicator("PUB-IND-01", "销售回款/营业收入", "增值税候选", "cash_received_from_sales", "operating_revenue", ("POL-VAT-2016-36",), "增值税申报表、销项发票、合同、回款明细", "POLICY_NEEDS_REVIEW"),
    PublicIndicator("PUB-IND-02", "应收账款/营业收入", "增值税候选", "accounts_receivable", "operating_revenue", ("POL-VAT-2016-36",), "客户合同、销项发票、收款及期后回款明细", "POLICY_NEEDS_REVIEW"),
    PublicIndicator("PUB-IND-03", "合同资产/营业收入", "增值税候选", "contract_assets", "operating_revenue", ("POL-VAT-2016-36",), "履约进度、验收资料、发票和增值税申报表", "POLICY_NEEDS_REVIEW"),
    PublicIndicator("PUB-IND-04", "合同负债/营业收入", "增值税候选", "contract_liabilities", "operating_revenue", ("POL-VAT-2016-36",), "预收款、合同履约、发票和增值税申报表", "POLICY_NEEDS_REVIEW"),
    PublicIndicator("PUB-IND-05", "研发费用/营业收入", "企业所得税候选", "research_and_development_expense", "operating_revenue", ("POL-CIT-RD-2023-07", "POL-CIT-RD-2023-11"), "研发项目书、辅助账、人员工时、企业所得税申报表及A107012", "POLICY_VERIFIED"),
    PublicIndicator("PUB-IND-06", "计入损益政府补助/营业收入", "企业所得税候选", "government_grants_recognized_in_profit", "operating_revenue", ("POL-CIT-GOV-2011-70",), "拨付文件、专项管理要求、单独核算资料及企业所得税申报表", "POLICY_VERIFIED"),
    PublicIndicator("PUB-IND-07", "税金及附加/营业收入", "多税种观察", "taxes_and_surcharges", "operating_revenue", (), "各税种明细账、纳税申报表、税费计算底稿"),
    PublicIndicator("PUB-IND-08", "支付各项税费/营业收入", "多税种观察", "taxes_paid", "operating_revenue", (), "税款缴款书、纳税申报表、税费明细账"),
    PublicIndicator("PUB-IND-09", "应交税费/营业收入", "多税种观察", "taxes_payable", "operating_revenue", (), "应交税费明细账、纳税申报表、缴款书"),
    PublicIndicator("PUB-IND-10", "营业成本/营业收入", "企业所得税候选", "operating_cost", "operating_revenue", (), "成本明细账、合同、发票、付款及企业所得税申报表"),
    PublicIndicator("PUB-IND-11", "应税合同与印花税凭证覆盖", "印花税候选", None, None, ("POL-STAMP-2022-14",), "应税合同台账、印花税税源明细表、申报表和缴款书", "POLICY_VERIFIED"),
    PublicIndicator("PUB-IND-12", "关联交易税务资料覆盖", "企业所得税候选", None, None, (), "关联交易明细、定价资料、合同、发票、资金流水及企业所得税申报表"),
)


def calculate_descriptive_observations(fields: pd.DataFrame) -> pd.DataFrame:
    """Return ratios and year-over-year changes without applying any risk threshold."""
    required_columns = {"period", "field", "amount_cny", "source_id"}
    if missing := required_columns - set(fields.columns):
        raise ValueError(f"missing public field columns: {sorted(missing)}")
    pivot = fields.pivot(index="period", columns="field", values="amount_cny").sort_index()
    source_ids = fields.groupby("period")["source_id"].first()
    rows: list[dict[str, object]] = []
    for indicator in INDICATORS:
        if not indicator.numerator or not indicator.denominator:
            continue
        if indicator.numerator not in pivot or indicator.denominator not in pivot:
            continue
        previous_value: float | None = None
        for period, values in pivot.iterrows():
            numerator = float(values[indicator.numerator])
            denominator = float(values[indicator.denominator])
            value = numerator / denominator if denominator else None
            rows.append(
                {
                    "indicator_id": indicator.indicator_id,
                    "indicator_name": indicator.name,
                    "period": str(period),
                    "candidate_tax_type": indicator.candidate_tax_type,
                    "value": value,
                    "previous_period_value": previous_value,
                    "change": value - previous_value if value is not None and previous_value is not None else None,
                    "formula": f"{indicator.numerator} / {indicator.denominator}",
                    "source_id": source_ids.loc[period],
                    "threshold_basis": "NONE_DESCRIPTIVE_LONGITUDINAL_COMPARISON_ONLY",
                    "status": "OBSERVATION",
                    "policy_ids": ";".join(indicator.policy_ids),
                    "policy_state": indicator.policy_state,
                    "evidence_required": indicator.evidence_required,
                    "conclusion_ceiling": "OBSERVATION; TODO_MISSING_DATA prevents tax-risk conclusion",
                }
            )
            previous_value = value
    return pd.DataFrame(rows)


def indicator_coverage(fields: pd.DataFrame) -> pd.DataFrame:
    available_fields = set(fields["field"])
    rows = []
    for indicator in INDICATORS:
        inputs = [value for value in (indicator.numerator, indicator.denominator) if value]
        available = bool(inputs) and all(value in available_fields for value in inputs)
        rows.append(
            {
                "indicator_id": indicator.indicator_id,
                "indicator_name": indicator.name,
                "candidate_tax_type": indicator.candidate_tax_type,
                "inputs": ";".join(inputs),
                "public_data_available": available,
                "status": "OBSERVATION_READY" if available else "TODO_MISSING_DATA",
                "policy_ids": ";".join(indicator.policy_ids),
                "policy_state": indicator.policy_state,
                "evidence_required": indicator.evidence_required,
                "conclusion_ceiling": "OBSERVATION" if available else "NO_CONCLUSION",
            }
        )
    return pd.DataFrame(rows)
