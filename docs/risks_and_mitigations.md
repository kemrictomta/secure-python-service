# Risks and Mitigations

## Overview

This document identifies technical, operational, and project risks for **secure-python-service** and defines mitigation strategies for each.

---

## 1. Risk Matrix

| # | Risk | Likelihood | Impact | Severity | Status |
|---|------|-----------|--------|----------|--------|
| R1 | No CI pipeline — regressions go undetected | High | High | **Critical** | Open |
| R2 | No entry point — project cannot be run | High | High | **Critical** | Open |
| R3 | Empty Dockerfile — cannot containerize | Medium | Medium | **High** | Open |
| R4 | Shallow validation — false positives/negatives | High | Medium | **High** | Open |
| R5 | No dependency pinning — build reproducibility | Medium | Medium | **High** | Open |
| R6 | No input size limits — resource exhaustion | Medium | High | **High** | Open |
| R7 | Low test coverage — undetected bugs | Medium | Medium | **Medium** | Open |
| R8 | No structured logging — difficult debugging | Medium | Low | **Medium** | Open |
| R9 | No documentation — poor onboarding | Medium | Low | **Medium** | Open |
| R10 | Scope creep to HTTP service — complexity | Low | Medium | **Low** | Open |

---

## 2. Detailed Risk Analysis

### R1: No CI Pipeline

**Description:** The `.github/workflows/ci.yml` file exists but is empty. No automated checks run on commits or pull requests.

**Impact:** Regressions, lint violations, and broken tests can be merged undetected.

**Mitigation:**
- [ ] Populate `ci.yml` with lint, type-check, and test steps
- [ ] Enable branch protection requiring CI to pass before merge
- [ ] Add test coverage minimum threshold (e.g., 80%)

---

### R2: No Entry Point

**Description:** `app/main.py` is empty. There is no `__main__.py` or CLI module. The project cannot be executed.

**Impact:** The tool provides no user-facing functionality.

**Mitigation:**
- [ ] Implement `app/cli.py` with `argparse`
- [ ] Wire `app/main.py` or `app/__main__.py` as entry point
- [ ] Define exit code mapping per architecture spec

---

### R3: Empty Dockerfile

**Description:** The Dockerfile is empty. No container image can be built.

**Impact:** Cannot deploy in containerized environments (Kubernetes, Docker Compose, CI runners).

**Mitigation:**
- [ ] Write a multi-stage Dockerfile with minimal base image
- [ ] Use non-root user for security
- [ ] Add `.dockerignore` to exclude unnecessary files

---

### R4: Shallow Validation

**Description:** The validator only checks if the payload is a dict and if 4 top-level keys exist. No type checking, no structure validation, no referential integrity.

**Impact:** Invalid models pass validation (false negatives). Users lose trust in the tool.

**Mitigation:**
- [ ] Add type validation for each field
- [ ] Validate node structure (`id`, `type`)
- [ ] Validate edge structure (`from`, `to`, `type`)
- [ ] Check edge references point to existing node IDs
- [ ] Detect duplicate node IDs

---

### R5: No Dependency Pinning

**Description:** `requirements.txt` is empty. No `pyproject.toml` exists.

**Impact:** Builds are not reproducible. Different environments may use different library versions.

**Mitigation:**
- [ ] Create `pyproject.toml` with pinned dependencies
- [ ] Use a lock file (`pip-compile` or `uv lock`)
- [ ] Pin Python version in CI and Dockerfile

---

### R6: No Input Size Limits

**Description:** No file size or payload depth limits are enforced. A malicious or accidentally large input could exhaust memory.

**Impact:** Denial of service (memory exhaustion, slow processing).

**Mitigation:**
- [ ] Add maximum file size check before loading (e.g., 10 MB)
- [ ] Limit JSON parsing recursion depth
- [ ] Limit maximum number of nodes/edges

---

### R7: Low Test Coverage

**Description:** Only 3 tests exist, covering the most basic paths. No edge cases, no integration tests, no property-based tests.

**Impact:** Bugs may exist in untested code paths, especially as validation logic deepens.

**Mitigation:**
- [ ] Add `pytest-cov` with coverage reporting
- [ ] Set minimum coverage threshold (80%+)
- [ ] Write edge-case tests: empty strings, wrong types, large payloads
- [ ] Add property-based tests with `hypothesis`

---

### R8: No Structured Logging

**Description:** No logging framework is configured. Errors and events are silent.

**Impact:** Debugging production issues is difficult. No audit trail.

**Mitigation:**
- [ ] Add Python `logging` module with configurable levels
- [ ] Log to stderr (keep stdout for report output)
- [ ] Add `--verbose` CLI flag

---

### R9: No Documentation

**Description:** `README.md` is empty. No usage instructions, no contributing guide, no changelog.

**Impact:** Poor developer onboarding. Users don't know how to use the tool.

**Mitigation:**
- [ ] Write README with quickstart, usage, and examples
- [ ] Add CHANGELOG.md
- [ ] Add LICENSE file
- [ ] Add CONTRIBUTING.md

---

### R10: Scope Creep to HTTP Service

**Description:** The architecture hints at a future HTTP API. Adding a web framework significantly increases complexity and attack surface.

**Impact:** Increased maintenance burden, security surface, and dependency count.

**Mitigation:**
- Mark HTTP API as explicitly out of scope for v1.0
- Only introduce if there is a validated use case
- If added, use a minimal framework (FastAPI) with strict input validation

---

## 3. Risk Response Summary

| Strategy | Risks |
|----------|-------|
| **Mitigate** | R1, R2, R3, R4, R5, R6, R7, R8, R9 |
| **Accept** | R10 (scope creep — monitor and defer) |

---

## 4. Risk Review Cadence

- Review risks at the start of each development sprint/phase
- Update severity and status as mitigations are implemented
- Add new risks as features are introduced

---

*Last updated: 2026-04-17*
