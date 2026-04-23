# Deployment Strategy

## Current State

No deployment mechanism exists. The Dockerfile and CI pipeline are empty placeholders.

---

## Deployment Targets

### Target 1: CLI Tool (Primary)

The tool is distributed as a Python package and run directly:

```bash
python -m app model.json
```

**Distribution options**:
- Install from source: `pip install .`
- Install from PyPI (future): `pip install secure-python-service`
- Run via Docker: `docker run secure-python-service model.json`

### Target 2: Docker Container

Used for CI integration and environments without Python installed.

**Planned Dockerfile** (multi-stage, minimal image):

```dockerfile
# --- Build stage ---
FROM python:3.12-slim AS builder
WORKDIR /build
COPY pyproject.toml .
COPY app/ app/
RUN pip install --no-cache-dir .

# --- Runtime stage ---
FROM python:3.12-slim
RUN useradd --create-home appuser
USER appuser
WORKDIR /home/appuser
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/
ENTRYPOINT ["python", "-m", "app"]
```

**Security considerations**:
- Non-root user.
- Minimal base image (`slim`, not `alpine` — avoids musl compatibility issues).
- No build tools in runtime image.
- Pinned base image digest (planned).

### Target 3: CI Pipeline Step (Future)

Integrate as a validation step in other repositories' CI pipelines:

```yaml
- name: Validate model
  run: |
    pip install secure-python-service
    python -m app models/service-graph.json
```

---

## CI/CD Pipeline (Planned)

### `.github/workflows/ci.yml`

```
Trigger: push to main, pull requests

Jobs:
  1. lint       → ruff check + ruff format --check
  2. typecheck  → mypy --strict app/
  3. test       → pytest --cov --cov-fail-under=80
  4. build      → docker build + smoke test
  5. publish    → (future) push to PyPI / GHCR on tag
```

### Branch Strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, always passing CI |
| `feature/*` | Development branches, merged via PR |
| `release/*` | Release preparation (future) |

---

## Versioning

- Semantic versioning (`MAJOR.MINOR.PATCH`).
- Version defined in `pyproject.toml`.
- Git tags trigger release builds.
- `CHANGELOG.md` maintained per release.

---

## Rollback Strategy

As a CLI tool (not a long-running service), rollback means pinning to a prior version:

```bash
pip install secure-python-service==1.0.0
```

Or using a tagged Docker image:

```bash
docker run secure-python-service:1.0.0 model.json
```

---

## Checklist Before First Release

- [ ] `pyproject.toml` with metadata and version
- [ ] Dockerfile builds and runs successfully
- [ ] CI pipeline passes (lint + type-check + test + build)
- [ ] README has usage instructions
- [ ] CHANGELOG has initial entry
- [ ] Git tag created for v0.1.0
