"""Run the reproducibility checks and record them as one workflow task."""
import subprocess
from pathlib import Path

from taxrisk.workflow import run_logged

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    with run_logged(
        "project_checks",
        "uv run python scripts/run_checks.py",
        "PHASE 0",
        ROOT,
    ) as run:
        for command in (["uv", "run", "ruff", "check", "."], ["uv", "run", "pytest", "--cov=taxrisk"]):
            completed = subprocess.run(command, cwd=ROOT, check=True, text=True)
            run.note(f"completed: {' '.join(command)}; returncode={completed.returncode}")
        print("project checks: PASS")


if __name__ == "__main__":
    main()
