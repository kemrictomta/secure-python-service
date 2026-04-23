# Project Overview

## Project Name

**secure-python-service**

## Summary

A Python-based CLI validation tool that accepts a JSON model describing a service graph (nodes and edges) and produces a structured validation report. The tool is designed to be deterministic, side-effect-free at its core, and easily extensible for future integrations (HTTP API, CI pipelines, etc.).

## Project Goals

1. Provide a reliable, automated way to validate JSON model definitions against a known schema.
2. Return clear, machine-readable validation reports with JSON-path-style error locations.
3. Maintain a clean separation of concerns: CLI → Loader → Validator → Domain → Renderer.
4. Serve as a foundation for production-grade tooling that can be embedded in CI/CD pipelines or exposed as a service.

## Current State

| Component | Status |
|---|---|
| Domain model (`Issue`, `Report`) | Implemented |
| Validator (`validate_model`) | Implemented — top-level field checks only |
| CLI (`app/cli.py`) | Not yet implemented |
| JSON Loader (`app/io.py`) | Not yet implemented |
| Entry point (`main.py` / `__main__.py`) | Not yet implemented |
| Report Renderer | Not yet implemented |
| Unit tests | 3 passing tests for validator |
| Dockerfile | Placeholder (empty) |
| CI/CD pipeline | Placeholder (empty) |
| Documentation | Architecture doc exists; README empty |

## Target Audience

- Developers building or maintaining service graph definitions.
- CI/CD systems that need automated pre-merge validation of model files.
- Platform teams who want to enforce structural consistency across service definitions.

## Technology Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Packaging | `pyproject.toml` (planned) |
| Testing | pytest |
| Containerization | Docker (planned) |
| CI/CD | GitHub Actions (planned) |
| Linting | ruff / mypy (planned) |
