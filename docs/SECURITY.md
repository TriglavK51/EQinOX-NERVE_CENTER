# Security

The default `mcp.json` policy denies external egress and the HTTP server rejects non-loopback binding.
Audit entries contain agent, tool, SHA-256 hashes, and HMAC signatures; raw request payloads and secrets are not logged.
Vault passphrases are accepted only from process environment or command arguments. Keep `state/` and `logs/` out of version control.