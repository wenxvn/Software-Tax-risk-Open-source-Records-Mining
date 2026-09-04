"""Inspect and update persistent workflow records."""
import argparse
from pathlib import Path

from taxrisk.workflow import WorkflowStore

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Tax-risk project workflow records")
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("status")
    phase = sub.add_parser("set-phase")
    phase.add_argument("phase")
    phase.add_argument("task")
    gate = sub.add_parser("gate")
    gate.add_argument("gate_id")
    gate.add_argument("status", choices=["NOT_STARTED", "IN_PROGRESS", "PASSED", "BLOCKED", "WAIVED"])
    gate.add_argument("--evidence", default="")
    gate.add_argument("--reviewer", default="")
    gate.add_argument("--notes", default="")
    args = parser.parse_args()
    store = WorkflowStore(ROOT)
    if args.action == "status":
        print(store.state_path.read_text(encoding="utf-8"), end="")
        print("-- gates --")
        print(store.gate_path.read_text(encoding="utf-8"), end="")
        print("-- recent tasks --")
        lines = store.log_path.read_text(encoding="utf-8").splitlines()
        print("\n".join(lines[-6:]))
    elif args.action == "set-phase":
        store.set_phase(args.phase, args.task)
        print(f"phase set: {args.phase} / {args.task}")
    else:
        store.set_gate(args.gate_id, args.status, args.evidence, args.reviewer, args.notes)
        print(f"gate set: {args.gate_id}={args.status}")


if __name__ == "__main__":
    main()

