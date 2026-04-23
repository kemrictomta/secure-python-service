# Security Design

## Overview

This document describes the security posture, threat model, and security controls for **secure-python-service**. As a CLI tool that processes untrusted JSON input, the primary concerns are input validation, resource limits, and dependency safety.

---

## 1. Current Security State

| Area | Status |
|------|--------|
| Input validation | Partial — type check and required field check only |
| Input size limits | **Not implemented** |
| Dependency scanning | **Not implemented** |
| SAST (static analysis) | **Not implemented** |
| Container security | **Not implemented** (Dockerfile is empty) |
| Secret management | N/A — no secrets used currently |
| Authentication | N/A — CLI tool, no auth needed |
| Authorization | N/A — local execution only |

---

## 2. Threat Model

### 2.1 Assets

| Asset | Description | Sensitivity |
|-------|-------------|-------------|
| JSON model input | User-provided data to validate | Low (public, NDA-safe) |
| Validation report | Output of the tool | Low |
| Source code | Project codebase | Medium |
| CI/CD pipeline | Build and test infrastructure | Medium |

### 2.2 Threat Actors

| Actor | Motivation | Capability |
|-------|-----------|------------|
| Careless user | Accidental large/malformed input | Low |
| Malicious user | Denial of service via crafted input | Medium |
| Supply chain attacker | Compromise via dependency | Medium |

### 2.3 Threats (STRIDE)

| Category | Threat | Applicable? | Description |
|----------|--------|-------------|-------------|
| **Spoofing** | Identity spoofing | No | CLI tool, no authentication |
| **Tampering** | Input tampering | Yes | Malformed JSON could crash the tool |
| **Repudiation** | Action denial | No | No user actions to repudiate |
| **Information Disclosure** | Data leakage | Low | Error messages could leak file paths |
| **Denial of Service** | Resource exhaustion | Yes | Large/deeply nested JSON payloads |
| **Elevation of Privilege** | Privilege escalation | No | Runs with user permissions only |

---

## 3. Security Controls

### 3.1 Input Validation (Partially Implemented)

**Current:**
- Payload must be a JSON object (dict)
- Required fields must be present

**Planned:**
```python
# [PLANNED] Input guards in Loader
import json
import os

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
MAX_JSON_DEPTH = 20

def safe_load(path: str) -> dict:
    # Guard: file size
    if os.path.getsize(path) > MAX_FILE_SIZE:
        raise InputError(f"File exceeds {MAX_FILE_SIZE} byte limit")

    with open(path, "r") as f:
        content = f.read()

    # Guard: parsing with depth limit
    return json.loads(content)  # Python's json module has no depth limit;
                                 # manual depth check or orjson required
```

### 3.2 Path Traversal Prevention (Planned)

```python
# [PLANNED] Ensure file path does not escape expected directory
import os

def validate_path(path: str, allowed_dir: str) -> str:
    real_path = os.path.realpath(path)
    if not real_path.startswith(os.path.realpath(allowed_dir)):
        raise InputError("Path traversal detected")
    return real_path
```

### 3.3 Error Message Safety

- **Do:** Return structured `Issue` objects with generic path references (`$.nodes[0].id`)
- **Don't:** Expose full filesystem paths, stack traces, or internal state in user-facing output
- **Planned:** Catch all exceptions at the CLI boundary and return safe error messages

### 3.4 Dependency Security (Planned)

| Tool | Purpose | Integration Point |
|------|---------|-------------------|
| `pip-audit` | Check for known vulnerabilities in Python packages | CI pipeline |
| `safety` | Alternative vulnerability scanner | CI pipeline |
| `bandit` | Python static security analysis (SAST) | CI pipeline, pre-commit hook |

### 3.5 Container Security (Planned)

| Control | Implementation |
|---------|---------------|
| Non-root user | `USER appuser` in Dockerfile |
| Minimal base image | `python:3.12-slim` or `distroless` |
| No shell in production | Use distroless or remove shell |
| Image scanning | `trivy` in CI pipeline |
| Read-only filesystem | `--read-only` Docker flag |

---

## 4. OWASP Top 10 Relevance

| OWASP Category | Relevant? | Controls |
|----------------|-----------|----------|
| A01: Broken Access Control | No | CLI tool, no access control |
| A02: Cryptographic Failures | No | No crypto operations |
| A03: Injection | Low | JSON parsing only, no SQL/shell |
| A04: Insecure Design | Yes | Pure function design mitigates this |
| A05: Security Misconfiguration | Yes | Docker and CI need proper config |
| A06: Vulnerable Components | Yes | Dependency scanning needed |
| A07: Auth Failures | No | No authentication |
| A08: Data Integrity Failures | Low | Validate input structure |
| A09: Logging Failures | Yes | No logging currently |
| A10: SSRF | No | No outbound network requests |

---

## 5. Secure Development Practices

### 5.1 Code Review Checklist

- [ ] No hardcoded secrets or credentials
- [ ] Input validated before processing
- [ ] Error messages don't leak internal details
- [ ] Dependencies pinned and scanned
- [ ] Tests cover security-relevant paths (malformed input, boundary values)

### 5.2 CI Security Gates (Planned)

```yaml
# [PLANNED] Security steps in ci.yml
- name: Security scan (bandit)
  run: bandit -r app/ -ll

- name: Dependency audit
  run: pip-audit --strict

- name: Container scan
  run: trivy image secure-python-service:latest
```

---

## 6. Implementation Roadmap

| # | Task | Priority | Status |
|---|------|----------|--------|
| 1 | Add file size limit in Loader | High | PLANNED |
| 2 | Add path traversal check | High | PLANNED |
| 3 | Sanitize error messages at CLI boundary | High | PLANNED |
| 4 | Add `bandit` to CI | Medium | PLANNED |
| 5 | Add `pip-audit` to CI | Medium | PLANNED |
| 6 | Write secure Dockerfile | Medium | PLANNED |
| 7 | Add `trivy` container scanning | Low | PLANNED |
| 8 | Evaluate JSON depth limiting | Low | PLANNED |

---

*Last updated: 2026-04-17*
