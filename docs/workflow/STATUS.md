# Workflow Status

这是项目的人工可读状态页。机器可读记录在同目录的 `workflow_state.json`、`TASK_LOG.csv`、`GATE_REGISTER.csv` 和 `EVENTS.jsonl`。

## 当前状态

- 当前阶段：PHASE 1（开源资料与候选案例筛选）
- 当前任务：基于已核验公开资料生成匿名化参赛提交文本（Word/PDF）
- 当前门禁：GATE A `IN_PROGRESS`；两期发行人年报的文件可追溯性已完成，仍缺企业内部资料，不得确认真实风险

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

## 提交文档生成

提交版由 `scripts/build_submission_document.py` 使用 `python-docx` 生成 Word 原生段落和可编辑表格，再使用 LibreOffice 从同一份 Word 导出 PDF。核心金额、比例和变动均从代码生成的 `outputs/tables/` 读取；不得在 Word 或 PDF 中手改数值。
