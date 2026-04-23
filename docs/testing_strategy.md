# Testing Strategy

## Philosophy

- Tests are first-class citizens — every validation rule has a corresponding test.
- The core validator is a pure function, making tests straightforward (no mocking required).
- Tests run fast (< 1s total) and are suitable for pre-commit and CI execution.

## Test Framework

- **pytest** — configured via `pytest.ini` with `pythonpath = .`.
- No additional test dependencies currently declared.

---

## Current Test Coverage

### `tests/test_validator.py` — 3 tests

| Test | What It Verifies |
|---|---|
| `test_invalid_payload_type` | Non-dict input returns `ok=False` with path `$` |
| `test_missing_required_fields` | Empty dict reports all 4 missing fields |
| `test_accepts_minimal_valid_payload` | Payload with all required fields returns `ok=True` |

### `tests/test_basic.py` — empty (placeholder)

---

## Test Pyramid Plan

```
         ┌──────────┐
         │   E2E    │   CLI invocation with real files
         ├──────────┤   (planned)
         │Integration│  Loader + Validator + Renderer chain
         ├──────────┤   (planned)
         │  Unit    │   Pure function tests (current focus)
         └──────────┘
```

### Unit Tests (Current + Planned)

| Category | Tests Needed | Status |
|---|---|---|
| Payload type check | Non-dict types (string, list, int, None) | Partial (string only) |
| Required fields | Missing each field individually | Planned |
| Field types | `name` not a string, `nodes` not a list, etc. | Planned |
| Node structure | Missing `id`, missing `type`, wrong types | Planned |
| Edge structure | Missing `from`/`to`/`type`, wrong types | Planned |
| Referential integrity | Edge references non-existent node | Planned |
| Node ID uniqueness | Duplicate `id` values | Planned |
| Valid payloads | Minimal valid, complex valid, empty nodes/edges | Partial |

### Integration Tests (Planned)

| Scenario | Description |
|---|---|
| Load valid file | File → Loader → Validator → Report(ok=True) |
| Load invalid JSON | Malformed JSON → InputError → exit code 2 |
| Load missing file | No file → InputError → exit code 2 |
| Full pipeline | File → Loader → Validator → Renderer → stdout |

### E2E / CLI Tests (Planned)

| Scenario | Description |
|---|---|
| Valid file | `python -m app valid.json` → exit 0, clean output |
| Invalid model | `python -m app bad.json` → exit 1, error report |
| Missing file | `python -m app nope.json` → exit 2, error message |
| JSON output | `python -m app bad.json --format json` → valid JSON |

---

## Test Tooling Plan

| Tool | Purpose | Status |
|---|---|---|
| pytest | Test runner | Configured |
| pytest-cov | Coverage reporting | Not installed |
| mypy | Static type checking (test files too) | Not configured |
| hypothesis | Property-based testing | Not installed |

## Coverage Target

- **Minimum**: 80% line coverage.
- **Goal**: 95%+ on `app/validator.py` and `app/domain.py`.
- Coverage gate to be enforced in CI once pipeline is set up.

## Running Tests

```bash
# Current
pytest

# Planned (with coverage)
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```
