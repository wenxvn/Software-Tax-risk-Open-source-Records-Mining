import csv
from pathlib import Path

from taxrisk.workflow import WorkflowStore


def test_workflow_records_run_and_gate(tmp_path: Path):
    store = WorkflowStore(tmp_path)
    tracker = store.start("test_task", "pytest", "PHASE TEST")
    tracker.add_output("out.csv")
    store.finish(tracker, "PASSED", "ok", tracker.outputs)
    store.set_gate("GATE_TEST", "PASSED", "out.csv")
    state = store.state()
    assert state["last_status"] == "PASSED"
    with store.log_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert rows[-1]["task"] == "test_task"
    assert rows[-1]["outputs"] == "out.csv"

