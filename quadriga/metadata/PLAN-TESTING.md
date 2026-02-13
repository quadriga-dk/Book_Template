# Plan: Metadata Scripts Test Suite

## Overview

Add comprehensive tests for the metadata transformation scripts in `quadriga/metadata/`.

**Current coverage**: 0% (no tests exist)
**Target coverage**: >80%

---

## Test Fixtures

Create `tests/fixtures/` with:

- `valid-metadata.yml` — all required fields, representative of a real project
- `minimal-metadata.yml` — only required fields, minimal valid values
- `invalid-metadata.yml` — missing required fields, wrong types, extra properties

---

## Test Files (in suggested implementation order)

| File | What it covers |
|------|---------------|
| `test_validate_schema.py` | Schema validation: valid/invalid/minimal metadata, network errors, missing jsonschema |
| `test_utils.py` | `load_yaml_file`, `save_yaml_file`, `extract_keywords`, `generate_citation_key`, `format_authors_for_bibtex`, `extract_first_heading` |
| `test_zenodo_json.py` | Zenodo JSON field mappings, required Zenodo fields |
| `test_jsonld.py` | JSON-LD output structure, schema.org compliance |
| `test_rdfxml.py` | RDF/XML output, Dublin Core mappings |
| `test_bibtex.py` | BibTeX format correctness, citation key format |
| `test_cff.py` | CITATION.cff field mappings |
| `test_data_flow.py` | End-to-end: metadata.yml → all output formats, no data loss |

---

## Open Questions

1. **pytest** needs to be added to `dev-requirements.txt`.

2. **Network dependency**: `validate_schema` fetches the QUADRIGA schema from a remote URL. Options:
   - **Mock network calls** — fast, works offline, but doesn't catch schema changes
   - **Hit real URL** — slower, needs network, but validates against actual schema
   - **Both**: fast mocked tests for CI + an optional integration test that hits the real URL
   - Suggestion: mock by default, add a marker like `@pytest.mark.network` for real-URL tests.

3. **GitHub Actions**: should tests run in the existing `update-metadata.yml` workflow or in a separate `test.yml` workflow? Separate seems cleaner — metadata updates shouldn't be blocked by unrelated test failures.

4. **Build order**: tests are most useful when written alongside the tasks that change each script (Zenodo verification, CRediT roles, etc.). Consider adding tests incrementally per task rather than all at once.

---

**Status**: Deferred — to be picked up as a dedicated effort.
