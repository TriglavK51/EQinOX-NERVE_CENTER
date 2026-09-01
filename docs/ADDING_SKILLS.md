# Adding Skills

Nerve Center discovers local skills from `tools/<tool_name>/tool.json`. No
central registration is required. `ToolRegistry` validates each manifest when
the service handles discovery or dispatch.

## Directory Contract

Create one directory per skill using lowercase letters, digits, and
underscores. Add a `THIRD_PARTY_LICENSES/` directory and an attribution file
when a skill incorporates or derives from a third-party implementation:

```text
tools/<tool_name>/
├── tool.json
├── server.py
└── tests/
    └── test_server.py
```

Use the shared local helper where its deterministic behavior is sufficient.
Create a dedicated implementation only when the skill needs behavior that the
helper cannot provide.

```python
from tools._common import meta, run_local_tool

NAME = "example_tool"


def run(input_data: dict) -> dict:
    return run_local_tool(NAME, input_data)


def health() -> dict:
    return meta(NAME)


def get_meta() -> dict:
    return meta(NAME)
```

Every server must expose `run(input_data: dict) -> dict`. It must return a JSON
object, behave deterministically in local mode, and never make a network call
unless a future approved policy explicitly enables it.

## Manifest Contract

`tool.json` requires all fields below. Names must be unique and match the tool
directory name.

```json
{
  "name": "example_tool",
    "category": "seo",
  "version": "1.1.0",
  "description": "Short, action-oriented local tool description.",
  "inputs": {"text": "string"},
  "outputs": {"report": "object"},
  "localOnly": true,
  "permissions": [],
  "costEstimate": "low"
}
```

Keep `localOnly` set to `true`. Declare every vault permission in
`permissions`; do not load a secret that is not declared. Input and output
schemas use simple JSON-compatible type labels such as `string`, `number`,
`boolean`, `array`, and `object`.

`category` is optional for compatibility and defaults to `uncategorized`; use
a lowercase alphanumeric identifier with underscores for new skills.

## Category Dispatch

Clients can run every local skill in a category in parallel:

```json
{
    "tool": "category",
    "input": {"category": "seo", "html": "<html>...</html>"}
}
```

Category execution is capped by `chainMaxDepth`, retains registry order in its
result, and is intended only for independent local tools that accept the same
input contract.

## Test Contract

Add a focused offline test:

```python
from tools.example_tool.server import run


def test_run_returns_local_result() -> None:
    result = run({"text": "example"})

    assert result["status"] == "ok"
    assert result["localOnly"] is True
```

Validate the change from the repository root:

```powershell
.\.venv\Scripts\python.exe -m black --check core vault tools tests mcp_server.py cli
.\.venv\Scripts\python.exe -m flake8 core vault tools tests mcp_server.py cli
.\.venv\Scripts\python.exe -m pytest -q
```

Restart `mcp_server.py` after adding a skill, then verify discovery and a real
dispatch:

```powershell
Invoke-RestMethod http://127.0.0.1:8088/.well-known/tools
```

## Optional Chain Integration

Add a recipe in `core/chain_builder.py` only if the new skill belongs to a
repeatable multi-tool workflow. Keep a chain at or below `chainMaxDepth` from
`mcp.json`; do not add a skill to a chain solely because it is available.

## Release Checklist

1. Add the directory, manifest, implementation, and test.
2. Run formatting, linting, tests, and the local API check.
3. Update `CHANGELOG.md` and the manifest version when releasing behavior.
4. Commit only generated runtime state that is intentionally part of the
   release. Never commit `.venv`, vault contents, audit logs, or cache files.