# Performance Considerations

## Overview

This document outlines the performance characteristics, constraints, and optimization strategies for **secure-python-service**. As a CLI-based JSON validator, the primary concerns are startup time, validation throughput, and memory usage for large payloads.

---

## 1. Current Performance Profile

| Aspect | Current State |
|--------|---------------|
| Startup time | Fast — pure Python, no heavy imports |
| Validation speed | O(n) where n = number of top-level fields checked |
| Memory usage | Minimal — payload loaded fully into memory |
| Concurrency | N/A — single-threaded CLI |
| Bottleneck | None at current scale (trivial validation) |

---

## 2. Performance Constraints

### 2.1 Input Size

| Parameter | Recommended Limit | Reason |
|-----------|-------------------|--------|
| JSON file size | < 10 MB | Avoid excessive memory usage |
| Number of nodes | < 10,000 | Keep validation time reasonable |
| Number of edges | < 50,000 | Edge reference checks are O(nodes * edges) if naive |
| Nesting depth | < 20 levels | Prevent stack overflow in recursive validation |

### 2.2 JSON Parsing

Python's built-in `json.loads()` is implemented in C and handles most payloads efficiently. For files exceeding 10 MB, consider:

- **`orjson`** — 3-10x faster JSON parsing (C extension)
- **`ijson`** — streaming parser for very large files (avoids loading entire file into memory)

**Current approach:** Standard `json` module (sufficient for expected payload sizes).

---

## 3. Validation Complexity

### 3.1 Current Validation (Implemented)

| Check | Complexity | Notes |
|-------|-----------|-------|
| Type check (is dict?) | O(1) | Constant time |
| Required field presence | O(k) | k = number of required fields (4) |

### 3.2 Planned Validation

| Check | Complexity | Optimization Strategy |
|-------|-----------|----------------------|
| Node structure validation | O(n) | Linear scan of nodes list |
| Edge structure validation | O(e) | Linear scan of edges list |
| Duplicate node ID detection | O(n) | Use a `set` for O(1) lookups |
| Edge reference integrity | O(e) | Build node ID set first, then check each edge — O(n + e) total |
| **Naive approach (avoid)** | O(n * e) | Checking each edge against all nodes without indexing |

### 3.3 Recommended Algorithm

```python
# [PLANNED] Efficient edge reference validation
def _check_edge_references(nodes: list, edges: list, issues: list) -> None:
    node_ids = {node["id"] for node in nodes}  # O(n)
    for i, edge in enumerate(edges):           # O(e)
        if edge.get("from") not in node_ids:
            issues.append(Issue(
                path=f"$.edges[{i}].from",
                message=f"Edge references unknown node: {edge.get('from')}",
            ))
```

**Total complexity:** O(n + e) — linear and scalable.

---

## 4. Memory Considerations

| Scenario | Memory Impact | Mitigation |
|----------|--------------|------------|
| Small payload (< 1 MB) | Negligible | None needed |
| Medium payload (1-10 MB) | ~3x file size in memory (raw + parsed + issues) | Acceptable |
| Large payload (> 10 MB) | May cause issues on constrained systems | Add file size check before loading |
| Adversarial payload (deep nesting) | Potential stack overflow | Limit `json.loads` recursion depth |

### Memory Safety

```python
# [PLANNED] Input size guard
import os

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def load_file(path: str) -> dict:
    size = os.path.getsize(path)
    if size > MAX_FILE_SIZE:
        raise InputError(f"File exceeds maximum size of {MAX_FILE_SIZE} bytes")
    ...
```

---

## 5. Startup Performance

| Component | Import Cost | Notes |
|-----------|------------|-------|
| `dataclasses` | ~1 ms | Standard library, very fast |
| `json` | ~1 ms | C-implemented, fast |
| `argparse` | ~2 ms | Standard library |
| `typing` | ~1 ms | Type hints only |
| **Total cold start** | **< 50 ms** | Acceptable for CLI tool |

No heavy dependencies (no NumPy, no web framework) — startup remains fast.

---

## 6. Benchmarking (Planned)

### 6.1 Benchmark Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Validation of 100-node model | < 10 ms | `time.perf_counter()` or `pytest-benchmark` |
| Validation of 10,000-node model | < 500 ms | Same |
| Memory for 10,000-node model | < 50 MB | `tracemalloc` |
| CLI cold start to exit | < 200 ms | `time` command |

### 6.2 Benchmark Tooling

- **`pytest-benchmark`** — for micro-benchmarks in test suite
- **`tracemalloc`** — for memory profiling
- **`time` command** — for end-to-end CLI timing

---

## 7. Optimization Roadmap

| # | Optimization | Priority | Status |
|---|-------------|----------|--------|
| 1 | Use `set` for node ID lookups | High | PLANNED |
| 2 | Add input file size limit | High | PLANNED |
| 3 | Limit JSON parsing recursion depth | Medium | PLANNED |
| 4 | Add benchmark suite | Medium | PLANNED |
| 5 | Evaluate `orjson` for large payloads | Low | PLANNED |
| 6 | Streaming validation for huge files | Low | PLANNED |

---

*Last updated: 2026-04-17*
