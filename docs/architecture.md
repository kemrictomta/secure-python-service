# Secure Python Service — Architecture

## Goal
Validate a public, NDA-safe JSON “model” and produce a human + machine readable report.

## Non-goals
- No company code or internal schemas
- No database integration yet
- No web server yet

## Inputs / Outputs
**Input:** JSON file path  
**Output:** exit code + text report (later JSON)

Exit codes:
- `0` valid
- `1` validation failed
- `2` input error (file/JSON)

## Components
1) **CLI (app/cli.py)**
- parses args
- orchestrates load → validate → render
- maps errors to exit codes

2) **Loader (app/io.py)**
- reads file
- parses JSON
- raises `InputError` with clear messages

3) **Validator (app/validator.py)**
- pure function: `validate(payload) -> Report`
- no printing, no IO

4) **Domain model (app/domain.py)**
- `Issue(path, message, severity)`
- `Report(ok, issues)`

5) **Renderer (optional later)**
- text renderer / json renderer

## Data format (public)
```json
{
  "name": "demo",
  "version": "1.0",
  "nodes": [{"id": "A", "type": "service"}],
  "edges": [{"from": "A", "to": "B", "type": "calls"}]
}
