# Architecture

`mcp_server.py` binds only to loopback and delegates POST `/run` requests to `Dispatcher`.
The dispatcher validates input, discovers `tools/*/tool.json`, resolves an executable recipe, imports only a validated local `server.py`, records signed input/output hashes, and persists execution outcomes.

The vault derives its AES-GCM key with scrypt each time from an argument or `NERVE_CENTER_VAULT_PASSPHRASE`; it never stores a master key.