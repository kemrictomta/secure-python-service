# Implementation

## Overview

This document describes the current implementation status and the planned implementation for each component of secure-python-service.

---

## Component: Domain Model (`app/domain.py`)

**Status**: Implemented

### Current Implementation

Two dataclasses define the validation output:

```python
@dataclass
class Issue:
    path: str          # JSON-path location (e.g., "$.name")
    message: str       # Human-readable description
    severity: str = "error"  # "error" | "warning" (future)

@dataclass
class Report:
    ok: bool           # True if no issues
    issues: list[Issue]
```

### Design Notes
- `severity` defaults to `"error"`, ready for future "warning" level.
- `Report.ok` is explicit rather than derived from `len(issues) == 0` for clarity.

---

## Component: Validator (`app/validator.py`)

**Status**: Partially implemented

### Current Implementation

`validate_model(payload: Any) -> Report` performs two checks:

1. **Type check** — ensures the payload is a `dict`.
2. **Required fields** — ensures `name`, `version`, `nodes`, `edges` are present.

### Planned Extensions

| Check | Priority | Status |
|---|---|---|
| Payload is a dict | P0 | Done |
| Required top-level fields | P0 | Done |
| `name` is a non-empty string | P1 | Planned |
| `version` is a valid string | P1 | Planned |
| `nodes` is a list of objects with `id` and `type` | P1 | Planned |
| `edges` is a list of objects with `from`, `to`, `type` | P1 | Planned |
| Node `id` uniqueness | P1 | Planned |
| Edge references valid node IDs | P1 | Planned |
| Warn on empty `nodes`/`edges` | P2 | Planned |

---

## Component: CLI (`app/cli.py`)

**Status**: Not implemented

### Planned Implementation

```
usage: secure-python-service [-h] [--format {text,json}] FILE

Validate a JSON model file.

positional arguments:
  FILE                  Path to JSON model file

optional arguments:
  -h, --help            show this help message and exit
  --format {text,json}  Output format (default: text)
```

- Uses `argparse` from stdlib.
- Orchestrates: parse args → load file → validate → render → exit.
- Maps exceptions to exit codes.

---

## Component: Loader (`app/io.py`)

**Status**: Not implemented

### Planned Implementation

```python
def load_model(path: str) -> dict:
    """Read and parse a JSON file. Raises InputError on failure."""
```

- Reads file with proper encoding (UTF-8).
- Catches `FileNotFoundError`, `PermissionError`, `json.JSONDecodeError`.
- Wraps all failures in a custom `InputError` with a clear message.

---

## Component: Entry Point (`app/main.py` or `__main__.py`)

**Status**: Not implemented

### Planned Implementation

- `app/main.py` or `app/__main__.py` wires CLI, Loader, Validator, and Renderer.
- Enables `python -m app <file>` invocation.

---

## Component: Renderer

**Status**: Not implemented

### Planned Implementation

Two renderers:

1. **Text renderer** — human-readable output for terminal use.
   ```
   Validation FAILED — 2 issues found:
     ERROR $.nodes[0].id — Missing required field: id
     ERROR $.edges[1].to — Reference to unknown node: Z
   ```

2. **JSON renderer** — structured output for CI/programmatic use.
   ```json
   {
     "ok": false,
     "issues": [
       {"path": "$.nodes[0].id", "message": "Missing required field: id", "severity": "error"}
     ]
   }
   ```

---

## File Map

| File | Role | Status |
|---|---|---|
| `app/__init__.py` | Package marker | Exists (empty) |
| `app/domain.py` | Domain model | Implemented |
| `app/validator.py` | Validation logic | Partial |
| `app/main.py` | Entry point | Placeholder |
| `app/cli.py` | CLI interface | Not created |
| `app/io.py` | File loader | Not created |
| `tests/test_validator.py` | Validator tests | 3 tests |
| `tests/test_basic.py` | General tests | Placeholder |
