# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Project Overview

FlakyTestHunter is a tool for detecting and analyzing flaky tests. The repo has:
- `backend/` — Python backend (app structure: `backend/app/bob/` and `backend/app/routes/`, currently empty scaffolding)
- `sample-target/` — A deliberately flaky Python app used as the test subject
- `frontend/` — Currently empty

## Commands

### Running the sample-target tests (from `sample-target/` directory)
```bash
# Activate venv first — required, no requirements.txt at root level
source venv/bin/activate

# Run all tests
pytest tests/

# Run a single test
pytest tests/test_app.py::test_process_order_succeeds
```

> **Critical**: Tests must be run from `sample-target/` (not the repo root) because `test_app.py` imports `from app import process_order` using a relative import with no package prefix. Running from repo root will cause `ModuleNotFoundError`.

## Architecture

### sample-target — Intentional Flakiness
- `sample-target/app.py`: `process_order()` sleeps `random.uniform(0, 0.3)` seconds, returns `{"status": "timeout"}` if delay > 0.2 — **this flakiness is intentional**, it's the subject under analysis.
- `sample-target/tests/test_app.py`: Tests `process_order` with no mocking, so it genuinely fails ~33% of the time by design.

### Backend scaffolding
- `backend/app/bob/` and `backend/app/routes/` directories exist but contain no files yet.

## Code Style (Python)

- Python 3.10 (venv pinned to 3.10.12)
- No linter config found; follow PEP 8
- No type annotations in existing code

## Testing

- Framework: **pytest** (installed in `sample-target/venv/`)
- No `pytest.ini` or `pyproject.toml` — pytest runs with defaults
- Test node ID format: `tests/test_app.py::test_process_order_succeeds`
