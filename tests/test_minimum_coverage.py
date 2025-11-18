from __future__ import annotations

from tests.utils.simple_coverage import CoverageSummary


def test_project_has_minimum_coverage(coverage_tracker) -> None:
    coverage_tracker.stop()
    summary: CoverageSummary = coverage_tracker.enforce_threshold()
    assert summary.percent >= coverage_tracker.minimum
