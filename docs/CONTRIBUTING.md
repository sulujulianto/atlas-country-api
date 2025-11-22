# Contributing Guide

## Local Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Coding Standards
- Follow PEP8; prefer type hints everywhere.
- Keep routes thin; business logic stays in services; repositories only handle data access.
- Maintain DTOs in `schemas/` and domain entities in `app/models/`.
- Use structured logging and preserve request IDs in logs.

## Testing
```bash
pytest --maxfail=1 --disable-warnings
```
- Aim for >=85% coverage.
- Add regression tests for new features and negative cases.

## Lint & Security
- Run `ruff` or `flake8`, `mypy`, `bandit` before PR.

## Git Workflow
- Feature branches + pull requests.
- Keep PRs focused; update `docs/CHANGELOG.md` for user-facing changes.
- Ensure README badges stay accurate when altering CI/coverage.

## Reporting Issues
- Include steps to reproduce, expected vs actual results, and logs (with request IDs if possible).
