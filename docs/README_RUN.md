# Run Nerve Center

Create a Python 3.11 virtual environment, install `pip install -e ".[dev]"`, and set `NERVE_CENTER_VAULT_PASSPHRASE` before using the vault.

Start the localhost-only service with `python mcp_server.py`. Discover tools at `http://127.0.0.1:8088/.well-known/tools`.

Run the local SEO fixture with `python cli/nervectl run --tool seo_technical --input tests/fixtures/sample_input.json`. The `pdf` tool deliberately returns a structured JSON fallback when no local renderer is configured.

Configure Claude-compatible clients with `claude.config.json`; the VS Code command performs HTTP discovery only.