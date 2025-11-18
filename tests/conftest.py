from __future__ import annotations

import os
from pathlib import Path
from typing import List

import pytest

from tests.utils.simple_coverage import SimpleCoverageTracker

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
MINIMUM_COVERAGE = float(os.environ.get("MIN_COVERAGE", "85"))
INCLUDED_FILES = [SRC_ROOT / "tools.py"]

COVERAGE_TRACKER = SimpleCoverageTracker(
    SRC_ROOT, minimum=MINIMUM_COVERAGE, include_files=INCLUDED_FILES
)
COVERAGE_TRACKER.start()


def pytest_collection_modifyitems(items: List[pytest.Item]) -> None:
    """Ensure the coverage assertion test is executed last."""

    coverage_items = [
        item
        for item in items
        if item.nodeid.endswith("test_minimum_coverage.py::test_project_has_minimum_coverage")
    ]
    for coverage_item in coverage_items:
        items.append(items.pop(items.index(coverage_item)))


@pytest.fixture(scope="session")
def coverage_tracker() -> SimpleCoverageTracker:
    return COVERAGE_TRACKER


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:  # pragma: no cover
    if not COVERAGE_TRACKER.finished:
        COVERAGE_TRACKER.stop()


def pytest_terminal_summary(terminalreporter, exitstatus: int, config) -> None:  # pragma: no cover
    if not COVERAGE_TRACKER.finished:
        return
    summary = COVERAGE_TRACKER.summary()
    terminalreporter.write_sep(
        "-", f"Simple coverage: {summary.percent:.2f}% (required {MINIMUM_COVERAGE:.2f}%)"
    )
    if summary.percent < MINIMUM_COVERAGE:
        terminalreporter.write_line(summary.format_missing())
    if os.environ.get("SIMPLE_COVERAGE_VERBOSE"):
        for file_summary in summary.files:
            terminalreporter.write_line(
                f"  {file_summary.path}: {file_summary.percent:.2f}% "
                f"({file_summary.executed}/{file_summary.executable})"
            )
    if os.environ.get("SIMPLE_COVERAGE_MISSING"):
        terminalreporter.write_line(summary.format_missing())
