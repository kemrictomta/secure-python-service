# Design Decisions

## DD-1: Pure Validation Function

**Decision**: The core validator (`validate_model`) is a pure function — no I/O, no printing, no side effects.

**Rationale**: Pure functions are trivially testable, composable, and reusable. The same function can be called from a CLI, an HTTP handler, or directly in tests without mocking.

**Trade-offs**: Requires a separate orchestration layer (CLI) to handle I/O, which adds complexity to the project structure.

**Status**: Implemented.

---

## DD-2: Dataclasses for Domain Model

**Decision**: Use Python `dataclasses` for `Issue` and `Report` rather than Pydantic models, TypedDicts, or plain dicts.

**Rationale**:
- Zero external dependencies (stdlib only).
- Provides type hints, `__eq__`, `__repr__` out of the box.
- Sufficient for the current data complexity.

**Trade-offs**: No built-in serialization to JSON (requires a manual renderer or `dataclasses.asdict`). No runtime type validation on construction.

**Status**: Implemented.

---

## DD-3: JSON-Path Error Locations

**Decision**: Validation issues reference their location using JSON-path-style strings (e.g., `$`, `$.name`, `$.nodes[0].id`).

**Rationale**: JSON-path is a widely understood notation. It allows consumers (humans and machines) to pinpoint exactly where in the payload the issue occurred.

**Trade-offs**: Requires constructing path strings during traversal, which adds minor complexity to deeper validation logic.

**Status**: Partially implemented (top-level paths only).

---

## DD-4: Collect All Errors Before Returning

**Decision**: The validator collects all issues into a list and returns them together, rather than failing on the first error.

**Rationale**: Fail-fast is frustrating for users who then have to fix one error and re-run repeatedly. Returning all issues at once enables faster iteration.

**Trade-offs**: Slightly more complex control flow; downstream issues may be cascading (e.g., if `nodes` is missing, edge reference checks are meaningless).

**Status**: Implemented.

---

## DD-5: Exit Code Convention

**Decision**: Three exit codes — `0` (valid), `1` (validation failed), `2` (input error — file not found, invalid JSON).

**Rationale**: Distinguishing "the model is invalid" from "we couldn't read the file" lets CI pipelines handle each case differently (e.g., retry on transient file errors).

**Trade-offs**: None significant.

**Status**: Not yet implemented (CLI not built).

---

## DD-6: No External Dependencies for Core

**Decision**: The core validation and domain layers use only Python stdlib.

**Rationale**: Minimizes supply-chain risk, keeps the Docker image small, and avoids version conflicts when embedded in larger projects.

**Trade-offs**: No access to Pydantic's schema validation, jsonschema, or other validation libraries that could reduce boilerplate.

**Status**: Current — no dependencies declared.

---

## DD-7: Separation of Concerns (5-Layer Architecture)

**Decision**: Decompose into CLI → Loader → Validator → Domain → Renderer.

**Rationale**: Each layer has a single responsibility. Changes to file I/O don't affect validation logic. Adding a new output format (JSON, SARIF) only requires a new renderer.

**Trade-offs**: More files and indirection than a single-script approach.

**Status**: Architecture documented; only Domain and Validator layers implemented.

---

## DD-8: Python 3.10+ Target

**Decision**: Use Python 3.10+ features (`list[T]` instead of `typing.List[T]`, `match` statements if needed).

**Rationale**: 3.10 is well past end-of-life risk, and the modern syntax is cleaner.

**Trade-offs**: Cannot run on Python 3.9 or earlier.

**Status**: Current — `list[Issue]` used in domain.py.
