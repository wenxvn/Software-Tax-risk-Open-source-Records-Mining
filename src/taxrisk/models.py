"""Validated records shared by ingestion, evidence, policy, and risk workflows."""
from datetime import date
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceRecord(BaseModel):
    source_id: str
    file_name: str
    file_hash: str
    source_type: str
    period: str | None = None
    received_date: date | None = None
    description: str | None = None
    confidentiality: str = "RESTRICTED"
    parser_status: str = "PENDING"


class LineageRecord(BaseModel):
    output_field: str
    source_file: str
    source_sheet: str | None = None
    source_field: str | None = None
    transformation: str
    formula: str | None = None
    code_reference: str | None = None


RiskStatus = Literal["OBSERVATION", "ANOMALY", "POTENTIAL_RISK", "NEED_TAX_REVIEW", "CONFIRMED_RISK", "CLEARED"]


class RiskRecord(BaseModel):
    risk_id: str
    rule_id: str
    tax_type: str
    business_process: str
    status: RiskStatus
    anomaly_score: float = Field(ge=0, le=1)
    risk_level: str = "UNASSESSED"
    amount: float | None = None
    policy_ids: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    reviewer_status: str = "PENDING"
    model_config = ConfigDict(extra="allow")


class EvidenceRecord(BaseModel):
    evidence_id: str
    risk_id: str
    evidence_type: str
    source_id: str
    location: str
    description: str
    supports: bool | None = None
    conflicts: bool = False
    verified: bool = False


class PolicyRecord(BaseModel):
    policy_id: str
    title: str
    document_number: str | None = None
    issuer: str
    publish_date: date | None = None
    effective_date: date | None = None
    expiry_date: date | None = None
    amendment_status: str | None = None
    article: str | None = None
    applicable_taxpayer: str | None = None
    applicable_business: str | None = None
    source_url: str
    verification_date: date | None = None
    case_period_applicable: bool | None = None
    notes: str | None = None
    status: Literal["VERIFIED", "NEEDS_REVIEW", "INVALID", "SUPERSEDED"] = "NEEDS_REVIEW"


def validate_rule_template(rule: dict[str, Any]) -> dict[str, Any]:
    required = {"rule_id", "name", "tax_type", "status", "inputs", "formula", "threshold", "policy_basis"}
    missing = required - rule.keys()
    if missing:
        raise ValueError(f"rule template missing fields: {sorted(missing)}")
    if rule["status"] != "TEMPLATE_ONLY":
        raise ValueError("initial rules must be TEMPLATE_ONLY")
    return rule

