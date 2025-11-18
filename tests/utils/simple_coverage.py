"""Minimal trace-based coverage tracker.

This module implements enough functionality to measure statement-level
coverage for the ``src`` package without relying on external dependencies
such as :mod:`coverage` or :mod:`pytest-cov`, which cannot be installed in
this execution environment.  The tracker is intentionally lightweight and
optimised for determinism so it can be used as part of the regular pytest
run.
"""
from __future__ import annotations

from dataclasses import dataclass
import ast
import os
from pathlib import Path
import sys
import threading
import trace
from typing import Dict, Iterable, List, Set


@dataclass(frozen=True)
class FileCoverage:
    """Coverage information for an individual source file."""

    path: Path
    executed: int
    executable: int
    missing: List[int]

    @property
    def percent(self) -> float:
        if self.executable == 0:
            return 100.0
        return 100.0 * self.executed / self.executable


@dataclass(frozen=True)
class CoverageSummary:
    """Aggregated coverage information for the project."""

    percent: float
    files: List[FileCoverage]

    def format_missing(self) -> str:
        """Return a deterministic multi-line missing lines summary."""

        lines = []
        for entry in sorted(self.files, key=lambda f: f.path):
            if not entry.missing:
                continue
            missing_ranges = _compress_line_numbers(entry.missing)
            lines.append(f"{entry.path}:{missing_ranges}")
        return "\n".join(lines)


class SimpleCoverageTracker:
    """Capture executed line information using :mod:`trace`."""

    def __init__(
        self,
        src_root: Path,
        minimum: float = 85.0,
        include_files: Iterable[Path] | None = None,
    ) -> None:
        self.src_root = src_root.resolve()
        self.minimum = minimum
        if include_files:
            resolved = [Path(path).resolve() for path in include_files]
            self._includes = tuple(resolved)
            self._includes_set = {path for path in resolved}
        else:
            self._includes = None
            self._includes_set: set[Path] | None = None
        self._tracer: trace.Trace | None = None
        self._counts: Dict[tuple[str, int], int] = {}
        self._summary: CoverageSummary | None = None
        self._enabled = False
        self._prev_trace = None
        self._prev_thread_trace = None
        self._finished = False

    @property
    def finished(self) -> bool:
        return self._finished

    def start(self) -> None:
        if self._enabled:
            return
        ignoredirs = self._build_ignoredirs()
        self._tracer = trace.Trace(count=True, trace=False, ignoredirs=ignoredirs)
        self._prev_trace = sys.gettrace()
        self._prev_thread_trace = threading.gettrace()
        sys.settrace(self._tracer.globaltrace)
        threading.settrace(self._tracer.globaltrace)
        self._enabled = True

    def stop(self) -> None:
        if not self._enabled:
            return
        sys.settrace(self._prev_trace)
        threading.settrace(self._prev_thread_trace)
        assert self._tracer is not None, "Tracer should exist when stopping"
        self._counts = dict(self._tracer.results().counts)
        self._enabled = False
        self._finished = True
        self._summary = None

    def summary(self) -> CoverageSummary:
        if not self._finished:
            raise RuntimeError("Coverage summary requested before tracker stopped")
        if self._summary is None:
            self._summary = self._compute_summary()
        return self._summary

    def enforce_threshold(self) -> CoverageSummary:
        summary = self.summary()
        if summary.percent < self.minimum:
            message = (
                f"Coverage {summary.percent:.2f}% is below the required "
                f"{self.minimum:.2f}%\n{summary.format_missing()}"
            )
            raise AssertionError(message)
        return summary

    def _build_ignoredirs(self) -> Iterable[str]:
        ignored = {sys.prefix, sys.exec_prefix}
        for env_var in ("VIRTUAL_ENV", "CONDA_PREFIX"):
            value = os.environ.get(env_var)
            if value:
                ignored.add(value)
        return tuple(str(Path(path).resolve()) for path in ignored if path)

    def _compute_summary(self) -> CoverageSummary:
        executed_by_file = self._executed_lines()
        file_reports: List[FileCoverage] = []
        total_executable = 0
        total_executed = 0

        file_iterable = self._includes if self._includes else self.src_root.rglob("*.py")
        for file_path in sorted(file_iterable):
            executable_lines = self._executable_lines(file_path)
            if not executable_lines:
                continue
            executed_lines = executed_by_file.get(str(file_path.resolve()), set())
            executed = len(executable_lines & executed_lines)
            file_total = len(executable_lines)
            missing = sorted(executable_lines - executed_lines)
            total_executable += file_total
            total_executed += executed
            file_reports.append(
                FileCoverage(
                    path=file_path.relative_to(self.src_root.parent),
                    executed=executed,
                    executable=file_total,
                    missing=missing,
                )
            )

        percent = 100.0
        if total_executable:
            percent = 100.0 * total_executed / total_executable
        return CoverageSummary(percent=percent, files=file_reports)

    def _executed_lines(self) -> Dict[str, Set[int]]:
        executed: Dict[str, Set[int]] = {}
        for (filename, lineno), _ in self._counts.items():
            path = Path(filename)
            try:
                resolved = path.resolve()
            except OSError:
                continue
            if self._includes_set is not None:
                if resolved not in self._includes_set:
                    continue
            elif not resolved.is_relative_to(self.src_root):
                continue
            executed.setdefault(str(resolved), set()).add(lineno)
        return executed

    def _executable_lines(self, path: Path) -> Set[int]:
        source = path.read_text(encoding="utf-8")
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return set()
        executable: Set[int] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.stmt):
                if isinstance(node, ast.Expr) and _is_docstring(node):
                    continue
                executable.add(node.lineno)
        for lineno, line in enumerate(source.splitlines(), start=1):
            if "# pragma: no cover" in line:
                executable.discard(lineno)
        return executable


def _compress_line_numbers(numbers: Iterable[int]) -> str:
    groups: List[str] = []
    numbers = sorted(set(numbers))
    for number in numbers:
        if not groups:
            groups.append(f"{number}")
            continue
        last = groups[-1]
        if "-" in last:
            start, end = map(int, last.split("-"))
        else:
            start = end = int(last)
        if number == end + 1:
            groups[-1] = f"{start}-{number}"
        else:
            groups.append(f"{number}")
    return ",".join(groups)


def _is_docstring(node: ast.Expr) -> bool:
    value = getattr(node, "value", None)
    return isinstance(value, ast.Constant) and isinstance(value.value, str)
