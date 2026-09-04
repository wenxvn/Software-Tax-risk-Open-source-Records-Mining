# 全国本科院校税收风险管控案例大赛

这是可复现的研究与分析基础设施，不是自动生成案例的工具。当前没有真实企业数据，所有真实结论均保持 TODO。

## 第一次使用

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
python scripts/inspect_raw_data.py
```

## 企业数据来了以后

将经授权的 Excel/CSV/PDF/Word、报表、申报、发票、合同、流水和订单放入 `data/raw/`（只读），再运行 `inspect_raw_data.py`、`build_data_dictionary.py`、`validate_data.py`。

## 政策与风险

官方原文放 `sources/policies/raw/`，文本放 `sources/policies/text/`，元数据登记 `sources/policies/index.csv`。依次运行 `run_reconciliation.py`、`run_risk_scan.py`、`audit_evidence.py`、`audit_policies.py` 和 `numeric_consistency_check.py`。

## Skills

在 Codex 中按 `$tax-risk-auditor`、`$policy-verifier`、`$evidence-auditor`、`$competition-red-team` 调用；若当前客户端尚未发现新 Skill，下一轮重启后再调用。完整阶段、输入、输出和 Gate 见 `docs/WORKFLOW.md`。

## 当前状态

见 `docs/PROJECT_STATUS.md`。下一步只需提供真实企业授权资料或确定案例企业，不能直接进入案例结论。

