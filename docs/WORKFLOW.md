# Competition Workflow

每个阶段均需通过 Gate 才能进入下一阶段；没有真实资料时只运行模板和合成测试。每次命令执行都会写入 `docs/workflow/`，因此可以中断后查看并恢复。

| Phase | 输入 | Skill/命令 | 输出 | 完成标准/门禁 | 记录 |
|---|---|---|---|---|
| 0 环境初始化 | 仓库 | 本 README、pytest | 工程与环境 | GATE A 基础可信 | TASK_LOG/GATE_REGISTER |
| 1 企业与行业选择 | 授权/规则 | 手工 + red-team | 企业与业务边界 | 不得虚构 | TASK_LOG/GATE_REGISTER |
| 2 原始资料收集 | 企业文件 | `inspect_raw_data.py` | raw、manifest | GATE A | TASK_LOG + manifest |
| 3 数据字典 | raw | `build_data_dictionary.py` | dictionaries | GATE B | TASK_LOG |
| 4 业务流程建模 | 访谈/制度 | tax-risk-auditor | 流程图/字段映射 | 可追溯 | TASK_LOG |
| 5 政策库 | 官方原文 | policy-verifier、`audit_policies.py` | index/text | GATE C | TASK_LOG + policy index |
| 6 候选规则 | 业务+政策 | tax-risk-auditor | rules | 仅候选 | TASK_LOG |
| 7 数据勾稽 | 标准化数据 | `run_reconciliation.py` | tables | 可复算 | TASK_LOG |
| 8 风险扫描 | 勾稽结果 | `run_risk_scan.py` | risks | GATE D | TASK_LOG |
| 9 假阳性排除 | 业务证据 | tax-risk-auditor | checks | GATE E | TASK_LOG |
| 10 证据审计 | 全部材料 | evidence-auditor、`audit_evidence.py` | evidence | GATE F | TASK_LOG |
| 11 确认与分级 | 审计结果 | tax-risk-auditor | register | 关键证据充分 | TASK_LOG/GATE_REGISTER |
| 12 整改方案 | 已确认风险 | tax-risk-auditor | remediation | 可执行 | TASK_LOG |
| 13 报告写作 | 机器结果 | 模板 | report/outputs | GATE G 数字一致 | TASK_LOG |
| 14 red-team | 报告全套 | competition-red-team | audit | GATE H 无 FATAL | TASK_LOG/GATE_REGISTER |
| 15 答辩材料 | 通过稿 | red-team | defense | 可解释可复算 | TASK_LOG |

阶段门：A 资料可信，B 数据完整，C 政策通过，D 计算可复现，E 假阳性完成，F 证据合格，G 数字一致，H 无 FATAL。

## 记录规则

- `docs/workflow/STATUS.md`：人工可读的当前阶段和恢复入口。
- `docs/workflow/workflow_state.json`：当前阶段、任务、最后一次运行状态。
- `docs/workflow/TASK_LOG.csv`：每次脚本的开始/结束、命令、状态和输出文件。
- `docs/workflow/EVENTS.jsonl`：追加式 START/NOTE/FINISH 事件，保留失败运行。
- `docs/workflow/GATE_REGISTER.csv`：每个 Gate 的状态、证据、审核人和备注。

查看状态：`uv run python scripts/workflow.py status`。切换阶段或登记 Gate：见 `docs/workflow/STATUS.md`。
