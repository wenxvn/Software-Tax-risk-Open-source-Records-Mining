---
name: policy-verifier
description: Verify tax policy records against official government sources and case-period applicability.
---

# Policy Verifier

Verify only official sources, prioritizing SAT, Ministry of Finance, gov.cn, and local tax authorities. Preserve the downloaded original in `sources/policies/raw/`, extracted text in `sources/policies/text/`, and register metadata in `sources/policies/index.csv`. Check repeal, supersession, dates, taxpayer identity, business applicability, and article accuracy. This skill validates policy; it does not write or beautify case reports.

Allowed statuses: `VERIFIED`, `NEEDS_REVIEW`, `INVALID`, `SUPERSEDED`. Missing or unverified policy is `POLICY_UNVERIFIED` in risk work.

