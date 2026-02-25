# Code Review: `project-ordinal`

## Overview

A NiceGUI web application for HKUST students to look up GPA ranks (852 students, Fall 2022 SENG cohort) and exam score percentiles (MATH1014, COMP2012H) using linear/cubic interpolation. Includes a PDF data extraction utility, Docker packaging, and an async test suite.

---

## Strengths

- **Clean architecture**: Well-separated concerns — data extraction (`analyzer.py`), web serving (`serve_website.py`), clear config-driven exam pages
- **Good tooling**: Ruff linting, mypy, pre-commit hooks, codespell — solid quality gates for a small project
- **Decent test coverage**: 11 async tests covering page loads, calculations, edge cases (best/worst rank), and navigation
- **Effective Dockerfile**: Proper layer caching with `requirements.txt` copied first, slim base image, no-cache pip install
- **DRY design**: Exam pages are driven from a configuration list with dynamic route registration, avoiding copy-paste

---

## Issues & Suggestions

### 1. Correctness / Bugs

- **Potential `IndexError` in exam score lookup** — `serve_website.py:236`: `idx = int(e.value / interp_step)` has no bounds check. A user entering `100` when `interp_step=1` gives `idx=100`, but if the percentile array has exactly 101 elements (indices 0-100), this is fine. However, entering `101` or a negative number will index out of range, and the bare `except Exception` silently swallows it showing just `'-'`. Consider adding explicit input validation instead of relying on try/except for control flow.

- **Bare `except Exception`** — `serve_website.py:239` and `serve_website.py:247`: These catch _all_ exceptions, hiding potential bugs. At minimum, catch `(IndexError, ValueError)` specifically.

- **Duplicate try/except blocks** — `serve_website.py:235-248`: The linear and cubic calculations repeat the same `idx` computation and catch logic. This could be a single try block or a helper.

- **`rank_range_top`/`rank_range_bottom` may be unbound** — `serve_website.py:148-156`: If `r720` is greater than all values in `rank720` but not in the list, the `for` loop sets these variables. But if `r720` is less than all values, the `else` branch handles it. If the list is empty (unlikely, but defensively), `rank_range_top` would be referenced before assignment at line 158.

- **Floating-point bin counts** — `serve_website.py:42`: COMP2012H has `bin_counts` like `6.5, 1.5, 4.5` which is unusual for student counts. This appears intentional (perhaps representing partial bin allocations) but deserves a comment explaining why.

### 2. Security

- **No input sanitization on the number fields**: NiceGUI handles this at the framework level (input type enforcement), so this is low-risk. Acceptable for this use case.

- **No sensitive data concerns**: The PDF data is already public (university briefing), and no authentication or user data is involved.

- **File path in `open('data_output.json')` is relative** — `serve_website.py:75`: Works because Docker sets `WORKDIR /app`, but could break if run from a different directory. Consider `Path(__file__).parent / 'data_output.json'`.

### 3. Performance

- **Good**: Percentile curves are pre-computed at startup (lines 67-72), so runtime lookups are O(1) array indexing.

- **`rank720.index(r720)` is O(n)** — `serve_website.py:141`: Linear scan on every GPA input change. With 852 elements this is fine, but for larger datasets a `bisect` lookup would be more appropriate. Acceptable at current scale.

### 4. Code Quality

- **Module-level side effects** — `analyzer.py:19-55`: The entire analyzer script runs at import time. It reads a PDF, does I/O, and writes a JSON file. If accidentally imported from another module, it would silently execute. Wrapping in `if __name__ == '__main__':` is the standard fix.

- **Untyped dictionaries for configuration** — The `EXAM_COURSES` list uses plain dicts with stringly-typed keys. A `dataclass` or `TypedDict` would provide IDE autocompletion and catch key typos at type-check time.

- **Magic numbers** — `720`, `3096`, `852` appear throughout without named constants. `720` is the GPA denominator, `3096` = `4.3 * 720`. A comment or constant would help readability.

- **`async def gpa_page` doesn't use `await`** — `serve_website.py:126`: The function is marked `async` but has no awaits. Same for the exam page wrapper at line 281. This works with NiceGUI but is semantically misleading.

### 5. Docker & Deployment

- **No version pinning in requirements.txt** — `requirements.txt:1-5`: `nicegui`, `numpy`, `scipy` are unpinned. A future `pip install` could pull breaking versions. Use `pip freeze` or a lock file for reproducible builds.

- **No health check in Dockerfile**: Consider adding `HEALTHCHECK` for production use.

- **No non-root user**: The container runs as root. Adding `RUN useradd -m app && USER app` is a best practice for production containers.

- **PDF bundled in image unnecessarily**: `major_selection_briefing_2023_dragged.pdf` (165KB) is copied into the Docker image but only used by `analyzer.py` (a one-time offline script). It should be added to `.dockerignore`.

### 6. Testing

- **No negative/boundary tests for exam pages**: Tests check that pages load and one lookup works, but don't test out-of-range inputs (negative scores, scores > 100), or verify the cubic interpolation result.

- **No test for `compute_percentiles`**: This is the core math function and should have a unit test with known inputs/outputs.

- **No test for the `count_run` helper**: Simple function, but worth a quick parameterized test.

- **`pdfminer` is not in requirements.txt**: `analyzer.py` imports `pdfminer`, but it's absent from `requirements.txt`. This is fine if `analyzer.py` is an offline-only tool, but should be documented.

### 7. Minor Nits

- `serve_website.py:114`: `str(c['nav_label'])` and `str(c['route'])` — these are already strings; the `str()` wrapping is unnecessary.
- `.dockerignore` excludes `Dockerfile` and `DOCKER.md` from the build context — good practice.
- `.gitignore` is minimal — consider adding `.ruff_cache/`, `.mypy_cache/`, `*.egg-info/`.

---

## Summary

| Area | Rating |
|------|--------|
| Correctness | Good — minor edge cases around unbounded input |
| Code Quality | Good — clean and DRY, would benefit from typed config and `__main__` guard |
| Security | Fine — no user data, framework handles input types |
| Performance | Good — precomputed data, O(1) lookups |
| Testing | Adequate — covers happy paths; missing boundary/unit tests for core math |
| Docker | Functional — needs version pinning and a non-root user for production |

**Overall**: A well-structured small project. The highest-value improvements would be (1) pinning dependency versions, (2) adding an `if __name__ == '__main__'` guard to `analyzer.py`, (3) catching specific exceptions instead of bare `except Exception`, and (4) adding the PDF to `.dockerignore`.
