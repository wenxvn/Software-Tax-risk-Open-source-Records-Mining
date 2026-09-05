# Workflow Status

这是项目的人工可读状态页。机器可读记录在同目录的 `workflow_state.json`、`TASK_LOG.csv`、`GATE_REGISTER.csv` 和 `EVENTS.jsonl`。

## 当前状态

- 当前阶段：PHASE 1（开源资料与候选案例筛选）
- 当前任务：归档官方政策候选并核验其在案例期间的适用边界
- 当前门禁：GATE A `IN_PROGRESS`；两期发行人年报的文件可追溯性已完成，仍缺企业内部资料与参赛资格确认，不得确认真实风险

## 如何查看

```bash
uv run python scripts/workflow.py status
```

## 如何更新阶段和 Gate

```bash
uv run python scripts/workflow.py set-phase "PHASE 1" "公开资料与候选企业筛选"
uv run python scripts/workflow.py gate GATE_A IN_PROGRESS --evidence "sources/curated/open_data/"
```

`TASK_LOG.csv` 为每次脚本运行的汇总记录，`EVENTS.jsonl` 为追加式事件记录；失败运行也必须保留。
