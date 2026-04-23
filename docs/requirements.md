# Requirements

## Functional Requirements

### FR-1: JSON Model Ingestion
- **FR-1.1**: The tool SHALL accept a file path to a JSON document as input.
- **FR-1.2**: The tool SHALL parse the JSON and report clear errors for invalid JSON syntax.
- **FR-1.3**: The tool SHALL report clear errors for missing or unreadable files.

### FR-2: Schema Validation
- **FR-2.1**: The tool SHALL verify the payload is a JSON object (not an array, string, etc.).
  - *Status: Implemented*
- **FR-2.2**: The tool SHALL verify the presence of required top-level fields: `name`, `version`, `nodes`, `edges`.
  - *Status: Implemented*
- **FR-2.3**: The tool SHALL verify `name` is a non-empty string.
  - *Status: Not implemented*
- **FR-2.4**: The tool SHALL verify `version` is a string matching a version pattern.
  - *Status: Not implemented*
- **FR-2.5**: The tool SHALL verify `nodes` is a list of objects, each containing at minimum `id` (string) and `type` (string).
  - *Status: Not implemented*
- **FR-2.6**: The tool SHALL verify `edges` is a list of objects, each containing at minimum `from` (string), `to` (string), and `type` (string).
  - *Status: Not implemented*

### FR-3: Referential Integrity
- **FR-3.1**: The tool SHALL verify that every `from` and `to` in `edges` references an existing node `id`.
  - *Status: Not implemented*
- **FR-3.2**: The tool SHALL verify that node `id` values are unique.
  - *Status: Not implemented*

### FR-4: Reporting
- **FR-4.1**: The tool SHALL return a `Report` object containing an `ok` boolean and a list of `Issue` objects.
  - *Status: Implemented*
- **FR-4.2**: Each `Issue` SHALL contain `path` (JSON-path), `message`, and `severity`.
  - *Status: Implemented*
- **FR-4.3**: The tool SHALL collect all issues before returning (not fail on first error).
  - *Status: Implemented*
- **FR-4.4**: The tool SHALL support text output for human readability.
  - *Status: Not implemented*
- **FR-4.5**: The tool SHALL support JSON output for machine consumption.
  - *Status: Not implemented*

### FR-5: CLI Interface
- **FR-5.1**: The tool SHALL provide a CLI accepting a file path argument.
  - *Status: Not implemented*
- **FR-5.2**: The tool SHALL exit with code `0` for valid models, `1` for validation failures, `2` for input errors.
  - *Status: Not implemented*

## Non-Functional Requirements

### NFR-1: Performance
- Validation SHALL complete in under 100ms for models with up to 1,000 nodes.

### NFR-2: Reliability
- The tool SHALL never crash on malformed input — all errors SHALL be caught and reported.

### NFR-3: Testability
- Core validation logic SHALL be a pure function with no side effects.
  - *Status: Implemented*

### NFR-4: Portability
- The tool SHALL run on Python 3.10+ with no external runtime dependencies for core validation.

### NFR-5: Security
- The tool SHALL not execute or eval any content from input files.
- Input size SHALL be bounded to prevent resource exhaustion (planned).

### NFR-6: Maintainability
- Code SHALL pass linting (ruff) and type checking (mypy) — *Not yet configured*.

## Traceability Matrix

| Requirement | Component | Test |
|---|---|---|
| FR-2.1 | `validator.py` | `test_invalid_payload_type` |
| FR-2.2 | `validator.py` | `test_missing_required_fields` |
| FR-4.1 | `domain.py` | `test_accepts_minimal_valid_payload` |
| FR-4.2 | `domain.py` | `test_invalid_payload_type` |
| FR-4.3 | `validator.py` | `test_missing_required_fields` |
