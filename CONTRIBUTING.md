# Contributing

Keep execution local by default. Do not add network calls without an explicit configuration gate.
Prefer streaming or bounded parsers, reuse local results, set timeouts, and avoid logging raw inputs or secrets.
Run `python -m pytest`, `black --check .`, `isort --check-only .`, and `flake8` before proposing changes.