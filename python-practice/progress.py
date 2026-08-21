#!/usr/bin/env python
"""
progress.py — your scoreboard.

Run it to see how many exercises you've completed:

    uv run python progress.py

It runs each module's test file separately and prints a tidy report.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TESTS_DIR = Path(__file__).parent / "tests"


def main() -> int:
    test_files = sorted(TESTS_DIR.glob("test_ex*.py"))
    if not test_files:
        print("No test files found. Are you in the project root?")
        return 1

    print("\n  Python Practice — Progress Report")
    print("  " + "=" * 40)

    done = 0
    for tf in test_files:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(tf), "-q", "--no-header"],
            capture_output=True,
            text=True,
        )
        passed = result.returncode == 0
        icon = "" if passed else "⬜"
        if passed:
            done += 1
        name = tf.stem.replace("test_", "")
        print(f"  {icon}  {name}")

    print("  " + "=" * 40)
    print(f"  {done}/{len(test_files)} modules complete\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
