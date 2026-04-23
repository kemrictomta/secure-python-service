# Architecture

## Overview

This document describes the architecture of **secure-python-service**, a Python CLI tool that validates public JSON models and produces structured validation reports.

---

## 1. Goal

Validate a public, NDA-safe JSON "model" describing a graph of services (nodes and edges) and produce a human- and machine-readable report.

---

## 2. Non-Goals

- No company code or internal schemas
- No database integration yet
- No web server yet (HTTP API is a future consideration)

---

## 3. System Context

```
+--------------+     JSON file      +----------------------------+
|   User       | -----------------> |  secure-python-service     |
|              | <-----------------  |  (CLI)                     |
+--------------+   exit code +      +----------------------------+
                   text/JSON report
```

---

## 4. Inputs / Outputs

**Input:** JSON file path (via CLI argument)
**Output:** exit code + text report (JSON output planned)

### Exit Codes

| Code | Meaning |
|------|---------|
| `0`  | Model is valid |
| `1`  | Validation failed (issues found) |
| `2`  | Input error (file not found, invalid JSON) |

---

## 5. Component Architecture

```
+-----------------------------------------------------+
|                    CLI (app/cli.py)                  |  [PLANNED]
|  - parses arguments                                 |
|  - orchestrates: load -> validate -> render          |
|  - maps errors to exit codes                        |
+-----------------------------------------------------+
|                  Loader (app/io.py)                  |  [PLANNED]
|  - reads file from disk                             |
|  - parses JSON                                      |
|  - raises InputError with clear messages            |
+-----------------------------------------------------+
|              Validator (app/validator.py)            |  IMPLEMENTED
|  - pure function: validate_model(payload) -> Report |
|  - no printing, no IO                               |
|  - currently: type check + required field check     |
+-----------------------------------------------------+
|             Domain Model (app/domain.py)            |  IMPLEMENTED
|  - Issue(path, message, severity)                   |
|  - Report(ok, issues)                               |
+-----------------------------------------------------+
|               Renderer (app/render.py)              |  [PLANNED]
|  - text renderer (human-readable)                   |
|  - JSON renderer (machine-readable)                 |
+-----------------------------------------------------+
```

### Component Status

| Component | File | Status |
|-----------|------|--------|
| CLI | `app/cli.py` | PLANNED |
| Loader | `app/io.py` | PLANNED |
| Validator | `app/validator.py` | Implemented (basic) |
| Domain | `app/domain.py` | Implemented |
| Renderer | `app/render.py` | PLANNED |
| Entry Point | `app/main.py` | Empty |

---

## 6. Data Flow

```
File Path -> [CLI] -> [Loader] -> JSON dict -> [Validator] -> Report -> [Renderer] -> Output
                                                  |
                                            Issue(path, message, severity)
```

1. **CLI** receives a file path argument
2. **Loader** reads the file and parses JSON; raises `InputError` on failure
3. **Validator** receives the parsed dict, runs validation rules, returns a `Report`
4. **Renderer** formats the `Report` as text or JSON
5. **CLI** maps the outcome to an exit code

---

## 7. Data Format (Public)

```json
{
  "name": "demo",
  "version": "1.0",
  "nodes": [{"id": "A", "type": "service"}],
  "edges": [{"from": "A", "to": "B", "type": "calls"}]
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | `string` | Model name |
| `version` | `string` | Model version |
| `nodes` | `list[object]` | Graph nodes (each with `id` and `type`) |
| `edges` | `list[object]` | Graph edges (each with `from`, `to`, `type`) |

---

## 8. Design Principles

1. **Pure functions over side effects** — validation logic never performs IO
2. **Separation of concerns** — each component has a single responsibility
3. **Fail fast with clear messages** — use JSON-path-style error paths (`$.nodes[0].id`)
4. **Testability first** — every component can be unit-tested in isolation
5. **Progressive enhancement** — start with CLI, add HTTP API later

---

## 9. Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Data modeling | `dataclasses` |
| Testing | `pytest` |
| Containerization | Docker (planned) |
| CI/CD | GitHub Actions (planned) |

---

*Last updated: 2026-04-17*
