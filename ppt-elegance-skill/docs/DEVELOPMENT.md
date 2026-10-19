# Development and release

## Structure

`SKILL.md` is agent-facing; READMEs are user-facing. `styles/` holds selectable visual rules. `references/` supplies content/layout/evidence guidance. `scripts/` implements spec validation, prompt compilation, the narrow synchronous API adapter and packaging. `examples/` contains original fictional inputs. `tests/` uses offline mocks and generated test fixtures, not paid API calls.

## Local tests

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python scripts/check_release.py
```

Packaging tests are skipped if optional dependencies are missing. Install requirements to exercise them. Never treat mocked transport success as verification of a real provider. No API credentials are required for these tests.

The development requirements include PyYAML for frontmatter validation. If you have the Skill Creator helper installed, its `quick_validate.py` can additionally validate the Skill folder; it is not a runtime dependency and is not bundled here.

## Extend

- Add style JSON and document it in the catalog. Test a cover, a diagram and a photo interior.
- Add modes or page types in `scripts/common.py` and the corresponding reference. Keep styles separate from source facts.
- Add providers as explicit adapters with capability declarations and tests. Keep secrets in environment variables, reject unintended redirects, document asynchronous semantics and avoid unbounded retries.
- Do not add a specific host's runtime path, provider credentials or private data to make an example convenient.

## Before publishing

1. Run tests and `scripts/check_release.py`; inspect the actual files, not only its report.
2. Confirm all included content can be distributed under the declared license. Do not commit third-party source templates or private project examples.
3. Confirm the MIT contributor attribution is appropriate for the actual authors; retain notices when incorporating others' work.
4. Keep real config, `.env`, generated outputs, source documents, caches and logs out of the repository. `.gitignore` does not remove already tracked content.
5. Inspect staged changes and any repository history for secrets. If secrets were ever published, revoke/rotate them before cleanup.
6. Create your own GitHub repository and upload this folder's contents. No repository URL or owner is preconfigured. This project does not publish automatically.

The release checker covers common accidental files, local links, forbidden machine paths and obvious key-shaped literals. It is a heuristic aid, not a comprehensive security or legal audit.

## Validation claims

Current release targets Python 3.10+ and image-based output. Report test results separately from image-service tests. A real service integration should identify its tested protocol/model configuration without recording credentials or confidential prompts. There is no claim that all services exposing `/images/generations` support the same fields.
