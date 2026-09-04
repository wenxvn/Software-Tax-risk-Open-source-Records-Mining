# Competition Workflow

每个阶段均需通过 Gate 才能进入下一阶段；没有真实资料时只运行模板和合成测试。

| Phase | 输入 | Skill/命令 | 输出 | 完成标准/门禁 |
|---|---|---|---|---|
| 0 环境初始化 | 仓库 | 本 README、pytest | 工程与环境 | GATE A 基础可信 |
| 1 企业与行业选择 | 授权/规则 | 手工 + red-team | 企业与业务边界 | 不得虚构 |
| 2 原始资料收集 | 企业文件 | `inspect_raw_data.py` | raw、manifest | GATE A |
| 3 数据字典 | raw | `build_data_dictionary.py` | dictionaries | GATE B |
| 4 业务流程建模 | 访谈/制度 | tax-risk-auditor | 流程图/字段映射 | 可追溯 |
| 5 政策库 | 官方原文 | policy-verifier、`audit_policies.py` | index/text | GATE C |
| 6 候选规则 | 业务+政策 | tax-risk-auditor | rules | 仅候选 |
| 7 数据勾稽 | 标准化数据 | `run_reconciliation.py` | tables | 可复算 |
| 8 风险扫描 | 勾稽结果 | `run_risk_scan.py` | risks | GATE D |
| 9 假阳性排除 | 业务证据 | tax-risk-auditor | checks | GATE E |
| 10 证据审计 | 全部材料 | evidence-auditor、`audit_evidence.py` | evidence | GATE F |
| 11 确认与分级 | 审计结果 | tax-risk-auditor | register | 关键证据充分 |
| 12 整改方案 | 已确认风险 | tax-risk-auditor | remediation | 可执行 |
| 13 报告写作 | 机器结果 | 模板 | report/outputs | GATE G 数字一致 |
| 14 red-team | 报告全套 | competition-red-team | audit | GATE H 无 FATAL |
| 15 答辩材料 | 通过稿 | red-team | defense | 可解释可复算 |

阶段门：A 资料可信，B 数据完整，C 政策通过，D 计算可复现，E 假阳性完成，F 证据合格，G 数字一致，H 无 FATAL。

