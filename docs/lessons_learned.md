# Lessons Learned

## Overview

This document captures insights, decisions, and takeaways gathered during the development of **secure-python-service**. It serves as a knowledge base for current and future contributors.

---

## 1. Architecture-First Approach

### What Worked
- Defining the architecture document (`docs/architecture.md`) before writing code gave clear direction for component boundaries.
- Separating the validator as a pure function made early testing straightforward.

### What Could Improve
- The architecture was partially aspirational — several planned components (CLI, Loader, Renderer) were not implemented. Keeping the architecture doc in sync with actual state would reduce confusion.

---

## 2. Domain Modeling with Dataclasses

### What Worked
- Using Python `dataclasses` for `Issue` and `Report` provided type safety, immutability hints, and clean `__repr__` output with minimal boilerplate.
- The `severity` field defaulting to `"error"` reduced noise in the common case.

### What Could Improve
- Consider using `@dataclass(frozen=True)` to enforce immutability.
- An enum for `severity` (`error`, `warning`, `info`) would prevent typos and enable filtering.

---

## 3. Testing Early

### What Worked
- Writing tests alongside the first validator function caught regressions immediately.
- The `pytest.ini` configuration with `pythonpath = .` was simple and effective for module resolution.

### What Could Improve
- Test coverage is limited to 3 tests covering only top-level validation. Edge cases (empty strings, wrong types for `nodes`/`edges`, deeply nested data) are untested.
- No test infrastructure for integration or end-to-end scenarios yet.

---

## 4. Project Scaffolding

### What Worked
- Setting up the directory structure (`app/`, `tests/`, `docs/`) early established clear conventions.

### What Could Improve
- Several scaffolded files (`main.py`, `Dockerfile`, `requirements.txt`, `README.md`, `ci.yml`) were left empty. Empty files can be misleading — they suggest functionality exists when it doesn't.
- A `pyproject.toml` would have been a better starting point than `requirements.txt` for modern Python projects.

---

## 5. Documentation Scope

### What Worked
- The architecture doc clearly defined inputs, outputs, exit codes, and component responsibilities.

### What Could Improve
- No README was written, making it hard for new contributors to onboard.
- Inline code documentation (docstrings) was minimal — only one docstring exists in `validator.py`.

---

## 6. Key Takeaways

| # | Lesson | Action |
|---|--------|--------|
| 1 | Define architecture early, but keep it aligned with reality | Mark unimplemented sections as `[PLANNED]` |
| 2 | Pure functions are the easiest to test and reason about | Continue this pattern for all business logic |
| 3 | Empty placeholder files can mislead | Either populate or remove them |
| 4 | Modern Python packaging (`pyproject.toml`) is preferable | Migrate from `requirements.txt` |
| 5 | CI should be set up before the first merge | Prioritize `.github/workflows/ci.yml` |
| 6 | Test coverage tooling should be added early | Integrate `pytest-cov` with thresholds |

---

## 7. Open Questions

- Should the project evolve into an HTTP service or remain a CLI tool?
- What is the expected maximum payload size? This affects validation performance strategy.
- Should the project support custom schema definitions in the future?

---

*Last updated: 2026-04-17*
