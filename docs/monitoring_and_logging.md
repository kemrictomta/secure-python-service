# Monitoring and Logging

## Overview

This document defines the monitoring and logging strategy for **secure-python-service**. As a CLI tool in its current form, the focus is on structured output and error reporting. If the project evolves into an HTTP service, this strategy will expand to include metrics, tracing, and alerting.

---

## 1. Current State

| Aspect | Status |
|--------|--------|
| Logging | **Not implemented** — no logging framework configured |
| Metrics | **Not applicable** — CLI tool, no runtime metrics |
| Tracing | **Not applicable** — single-process, no distributed tracing |
| Error reporting | Partial — `Report` / `Issue` dataclasses capture validation errors |

---

## 2. Logging Strategy

### 2.1 Logging Levels

| Level | Usage |
|-------|-------|
| `DEBUG` | Detailed validation steps, parsed payload structure |
| `INFO` | File loaded, validation started/completed, report summary |
| `WARNING` | Non-critical validation issues (e.g., isolated nodes) |
| `ERROR` | Validation failures, malformed input |
| `CRITICAL` | Unexpected exceptions, unrecoverable errors |

### 2.2 Planned Implementation

```python
# [PLANNED] app/logging_config.py
import logging
import sys

def setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        stream=sys.stderr,
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
```

### 2.3 Logging Guidelines

- **Log to stderr** — keep stdout clean for report output (text/JSON)
- **Structured fields** — include file path, validation duration, issue count
- **No sensitive data** — never log payload content beyond field names
- **CLI verbosity flag** — `--verbose` / `-v` to enable DEBUG level

---

## 3. Output Reporting (Current Mechanism)

The `Report` dataclass is the primary output mechanism:

```python
@dataclass
class Report:
    ok: bool
    issues: list[Issue]  # Each issue has path, message, severity
```

### Exit Code Mapping

| Exit Code | Meaning | Log Level |
|-----------|---------|-----------|
| `0` | Valid model | INFO |
| `1` | Validation failed | ERROR |
| `2` | Input error (file/JSON) | ERROR |

---

## 4. Future: Service-Mode Monitoring

### 4.1 Metrics (Planned — if HTTP API is added)

| Metric | Type | Description |
|--------|------|-------------|
| `validation_requests_total` | Counter | Total validation requests |
| `validation_errors_total` | Counter | Requests that failed validation |
| `validation_duration_seconds` | Histogram | Time spent validating |
| `input_errors_total` | Counter | Malformed/unparseable inputs |

**Tooling:** Prometheus client library (`prometheus-client`)

### 4.2 Health Checks (Planned)

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Liveness — is the process running? |
| `GET /ready` | Readiness — is the service ready to accept requests? |

### 4.3 Distributed Tracing (Planned)

- **Standard:** OpenTelemetry
- **Use case:** If the validator is called as part of a larger pipeline, trace context propagation enables end-to-end visibility

---

## 5. Alerting (Planned)

| Alert | Condition | Severity |
|-------|-----------|----------|
| High error rate | >10% of requests return exit code 2 | Warning |
| Validation latency spike | p99 > 500ms | Warning |
| Process crash | Unexpected exit code | Critical |

---

## 6. Implementation Roadmap

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | Add `logging` module to CLI | High | PLANNED |
| 2 | Add `--verbose` flag | High | PLANNED |
| 3 | Log to stderr, report to stdout | High | PLANNED |
| 4 | Structured JSON logging (`structlog`) | Medium | PLANNED |
| 5 | Prometheus metrics (service mode) | Low | PLANNED |
| 6 | OpenTelemetry tracing | Low | PLANNED |

---

*Last updated: 2026-04-17*
