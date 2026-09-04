---
name: tax-risk-auditor
description: Scan real enterprise tax data with reproducible reconciliation, anomaly detection, evidence checks, and staged risk conclusions.
---

# Tax Risk Auditor

Use only supplied enterprise records. Follow: business understanding -> completeness -> normalization -> reconciliation -> rule/indicator calculation -> anomaly -> potential risk -> false-positive checks -> evidence and policy verification -> confirmation -> grading -> remediation -> monitoring.

Never invent facts, thresholds, amounts, or policies. Missing source material is `TODO_MISSING_DATA`; uncertain tax treatment is `NEED_TAX_REVIEW`; an unexplained deviation remains `ANOMALY`. Never jump from anomaly to confirmed risk. Every result must carry source fields, formula, threshold basis, policy IDs, evidence IDs, and reproducible code output.

See [risk_schema.md](references/risk_schema.md) for the required risk record.

