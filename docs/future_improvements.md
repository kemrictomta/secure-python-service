# Future Improvements

## Overview

This document outlines planned enhancements and long-term evolution goals for **secure-python-service**, organized by priority and engineering phase.

---

## 1. Short-Term (Next Sprint)

### 1.1 Complete Core Components

| Component | File | Status | Description |
|-----------|------|--------|-------------|
| CLI | `app/cli.py` | **PLANNED** | Argument parsing with `argparse`, exit code mapping (0/1/2) |
| Loader | `app/io.py` | **PLANNED** | File reading, JSON parsing, `InputError` exceptions |
| Entry Point | `app/main.py` | **PLANNED** | Wire CLI → Loader → Validator → Output |
| `__main__` | `app/__main__.py` | **PLANNED** | Enable `python -m app` invocation |

### 1.2 Deepen Validation Logic

- **Type validation** — verify `name` is `str`, `version` is `str`, `nodes` is `list`, `edges` is `list`
- **Node structure** — each node must have `id` (str) and `type` (str)
- **Edge structure** — each edge must have `from` (str), `to` (str), and `type` (str)
- **Referential integrity** — every edge endpoint must reference an existing node `id`
- **Duplicate detection** — flag duplicate node IDs
- **Severity levels** — distinguish `error` vs `warning` (e.g., isolated nodes could be warnings)

### 1.3 Populate Build Files

- Write `requirements.txt` or `pyproject.toml` with pinned dependencies
- Write `Dockerfile` with multi-stage build, non-root user, minimal base image
- Write `README.md` with purpose, quickstart, usage, and contributing sections

---

## 2. Medium-Term (1–2 Months)

### 2.1 Report Rendering

- **Text renderer** — human-readable console output with color support
- **JSON renderer** — machine-readable structured output for tooling integration
- **Renderer interface** — pluggable renderers selected via CLI flag (`--format text|json`)

### 2.2 CI/CD Pipeline

- Populate `.github/workflows/ci.yml`:
  - Lint (`ruff`)
  - Type check (`mypy --strict`)
  - Test (`pytest --cov`)
  - Build Docker image
  - Publish coverage report
- Add branch protection rules documentation
- Add release workflow with semantic versioning

### 2.3 Code Quality Tooling

- **Linting** — `ruff` configuration in `pyproject.toml`
- **Type checking** — `mypy` with strict mode
- **Pre-commit hooks** — `.pre-commit-config.yaml` with ruff, mypy, trailing whitespace checks
- **Test coverage** — `pytest-cov` with minimum threshold (e.g., 90%)

### 2.4 Error Handling

- Custom exception hierarchy:
  - `InputError` — file not found, permission denied, invalid JSON
  - `ValidationError` — schema violations (distinct from `Issue` reporting)
- Consistent error message format across all components

---

## 3. Long-Term (3–6 Months)

### 3.1 HTTP API (Optional Service Mode)

- **Framework** — FastAPI for async support and automatic OpenAPI docs
- **Endpoints**:
  - `POST /validate` — accept JSON body, return `Report`
  - `GET /health` — liveness check
  - `GET /ready` — readiness check (dependency verification)
- **Input limits** — max payload size, request rate limiting
- **API versioning** — `/v1/validate`

### 3.2 Observability

- **Structured logging** — `structlog` with JSON output for log aggregation
- **Metrics** — Prometheus-compatible metrics (validation count, error rate, latency)
- **Tracing** — OpenTelemetry integration for distributed tracing (if service mode)

### 3.3 Security Hardening

- **Dependency scanning** — `safety` or `pip-audit` in CI
- **SAST** — `bandit` for Python security linting
- **Container scanning** — `trivy` for Docker image vulnerabilities
- **Input sanitization** — payload size limits, recursion depth limits for JSON parsing
- **Secret management** — environment-based configuration, no hardcoded secrets

### 3.4 Advanced Validation Features

- **Custom schema support** — allow users to define their own node/edge schemas via config files
- **Schema versioning** — support multiple data format versions
- **Cross-model validation** — validate relationships between multiple model files
- **Performance optimization** — streaming validation for large payloads

### 3.5 Packaging & Distribution

- Publish to PyPI as an installable CLI tool
- Publish Docker image to container registry (GHCR or Docker Hub)
- Homebrew formula for macOS users

---

## 4. Improvement Backlog

| # | Improvement | Priority | Effort | Phase |
|---|------------|----------|--------|-------|
| 1 | Implement CLI + Loader | High | Small | Short |
| 2 | Deep validation (nodes, edges, refs) | High | Medium | Short |
| 3 | Dockerfile + requirements.txt | High | Small | Short |
| 4 | CI pipeline (lint, test, build) | High | Small | Medium |
| 5 | Text + JSON renderers | Medium | Small | Medium |
| 6 | mypy strict + ruff config | Medium | Small | Medium |
| 7 | Test coverage ≥ 90% | Medium | Medium | Medium |
| 8 | README + CHANGELOG | Medium | Small | Medium |
| 9 | FastAPI service mode | Low | Large | Long |
| 10 | Structured logging + metrics | Low | Medium | Long |
| 11 | Custom schema support | Low | Large | Long |
| 12 | PyPI / GHCR publishing | Low | Medium | Long |

---

## 5. Non-Goals (Explicitly Out of Scope)

- Database integration
- User authentication / authorization
- Multi-tenancy
- Internal or proprietary schema support
- GUI / web frontend

---

*Last updated: 2026-04-17*
