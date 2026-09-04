"""Persistent, append-only workflow execution records."""
from __future__ import annotations

import csv
import json
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterator


LOG_FIELDS = [
    "run_id",
    "started_at",
    "finished_at",
    "phase",
    "task",
    "command",
    "status",
    "message",
    "outputs",
]
GATE_FIELDS = ["gate_id", "status", "updated_at", "evidence", "reviewer", "notes"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class WorkflowStore:
    def __init__(self, root: str | Path = ".") -> None:
        self.root = Path(root).resolve()
        self.directory = self.root / "docs" / "workflow"
        self.directory.mkdir(parents=True, exist_ok=True)
        self.log_path = self.directory / "TASK_LOG.csv"
        self.gate_path = self.directory / "GATE_REGISTER.csv"
        self.state_path = self.directory / "workflow_state.json"
        self.events_path = self.directory / "EVENTS.jsonl"
        self._ensure_csv(self.log_path, LOG_FIELDS)
        self._ensure_csv(self.gate_path, GATE_FIELDS)
        if not self.state_path.exists():
            self._write_state(
                {
                    "current_phase": "PHASE 0",
                    "current_task": "环境初始化",
                    "last_run_id": None,
                    "last_status": "NOT_STARTED",
                    "updated_at": _now(),
                }
            )

    @staticmethod
    def _ensure_csv(path: Path, fields: list[str]) -> None:
        if not path.exists():
            with path.open("w", newline="", encoding="utf-8") as handle:
                csv.DictWriter(handle, fieldnames=fields).writeheader()

    def _write_state(self, state: dict[str, object]) -> None:
        self.state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def _event(self, event: dict[str, object]) -> None:
        with self.events_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")

    def start(self, task: str, command: str, phase: str) -> "RunTracker":
        run_id = f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{uuid.uuid4().hex[:8]}"
        started = _now()
        tracker = RunTracker(self, run_id, task, command, phase, started)
        self._event({"event": "START", "run_id": run_id, "at": started, "phase": phase, "task": task})
        self._write_state(
            {
                "current_phase": phase,
                "current_task": task,
                "last_run_id": run_id,
                "last_status": "RUNNING",
                "updated_at": started,
            }
        )
        return tracker

    def finish(self, tracker: "RunTracker", status: str, message: str = "", outputs: list[str] | None = None) -> None:
        finished = _now()
        with self.log_path.open("a", newline="", encoding="utf-8") as handle:
            csv.DictWriter(handle, fieldnames=LOG_FIELDS).writerow(
                {
                    "run_id": tracker.run_id,
                    "started_at": tracker.started,
                    "finished_at": finished,
                    "phase": tracker.phase,
                    "task": tracker.task,
                    "command": tracker.command,
                    "status": status,
                    "message": message,
                    "outputs": ";".join(outputs or []),
                }
            )
        self._event({"event": "FINISH", "run_id": tracker.run_id, "at": finished, "status": status, "message": message})
        state = self.state()
        state.update({"last_run_id": tracker.run_id, "last_status": status, "updated_at": finished})
        self._write_state(state)

    def state(self) -> dict[str, object]:
        return json.loads(self.state_path.read_text(encoding="utf-8"))

    def set_phase(self, phase: str, task: str) -> None:
        state = self.state()
        state.update({"current_phase": phase, "current_task": task, "updated_at": _now()})
        self._write_state(state)

    def set_gate(self, gate_id: str, status: str, evidence: str = "", reviewer: str = "", notes: str = "") -> None:
        rows: list[dict[str, str]] = []
        with self.gate_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        row = {"gate_id": gate_id, "status": status, "updated_at": _now(), "evidence": evidence, "reviewer": reviewer, "notes": notes}
        rows = [existing for existing in rows if existing.get("gate_id") != gate_id] + [row]
        with self.gate_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=GATE_FIELDS)
            writer.writeheader()
            writer.writerows(rows)


class RunTracker:
    def __init__(self, store: WorkflowStore, run_id: str, task: str, command: str, phase: str, started: str) -> None:
        self.store = store
        self.run_id = run_id
        self.task = task
        self.command = command
        self.phase = phase
        self.started = started
        self.outputs: list[str] = []

    def add_output(self, path: str | Path) -> None:
        self.outputs.append(str(path))

    def note(self, message: str) -> None:
        self.store._event({"event": "NOTE", "run_id": self.run_id, "at": _now(), "message": message})


@contextmanager
def run_logged(task: str, command: str, phase: str, root: str | Path = ".") -> Iterator[RunTracker]:
    store = WorkflowStore(root)
    tracker = store.start(task, command, phase)
    try:
        yield tracker
    except Exception as exc:
        store.finish(tracker, "FAILED", f"{type(exc).__name__}: {exc}", tracker.outputs)
        raise
    else:
        store.finish(tracker, "PASSED", "", tracker.outputs)

