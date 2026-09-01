# 🧠 Nerve-Center

**Autonomous Tool-Routing Intelligence for Claude Code**

> *Think like a human. Execute like a machine. Evolve like life.*

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Platform-Claude_Code-blueviolet.svg)]()
[![EQinOX](https://img.shields.io/badge/by-EQinOX-orange.svg)]()

---

## What is Nerve-Center?

Nerve-Center is a **self-evolving AI skill** that automatically detects which tools, skills, plugins, and extensions should fire for any given task in Claude Code — and chains them together for maximum effectiveness at minimum token cost.

**No commands. No slash-prefixes. No memorization.** You just ask — and Nerve-Center figures out the rest.

### The Problem

Claude Code has hundreds of available skills and plugins. Nobody remembers which one does what. Users either:
- Use the wrong tool and get suboptimal results
- Use no tool at all and miss powerful automation
- Manually chain tools when a single command could do it

### The Solution

Nerve-Center sits between the user and the tool catalog. It:

1. **Reads intent** — understands what you actually want, not just what you typed
2. **Scores every tool** — using a 4-factor matrix (relevance, cost, speed, track record)
3. **Dispatches the best one** — or chains multiple tools when that's faster/cheaper
4. **Learns from outcomes** — records what worked, what didn't, and evolves its own logic
5. **Stays silent** — you see results, not routing decisions (unless you ask)

---

## Installation

### Windows and VS Code Workspaces

From the repository root, run one command to create or update the local Python
environment, install dependencies, and start the localhost-only API:

```powershell
.\setup.ps1 -Start
```

For a repeatable agent workflow in a new workspace, use the
[workspace integration guide](docs/WORKSPACE_INTEGRATION.md) and its
[`PLAN_PRACY` template](templates/PLAN_PRACY.md).

### Claude Code (User Skills)
```bash
# Copy the nerve-center/ directory to your skills folder
cp -r nerve-center/ ~/.claude/skills/nerve-center/
```

### Claude Code (Project Skills)
```bash
# Place in your project's .claude/ directory
cp -r nerve-center/ .claude/skills/nerve-center/
```

### Manual
Just place the `nerve-center/` folder anywhere Claude Code can read `.md` files from its skill directories.

---

## How It Works

### Adding a local tool

Each skill lives in `tools/<tool_name>/`. Add a compact `tool.json` manifest
that declares its category, inputs, outputs, permissions, and `localOnly: true`,
then expose `run(input_data: dict) -> dict` from `server.py`. `ToolRegistry`
discovers and validates the manifest automatically; no dispatcher registration
is needed. JSON is the runtime index for fast discovery, while Markdown is used
for human-facing instructions, attribution, and license records.

Skills sharing a category can be invoked together with `tool: "category"`; the
local dispatcher executes their independent adapters in parallel, capped by the
configured chain depth.

### Free Local API Connections

`openserp` connects to a self-hosted OpenSERP instance at
`http://127.0.0.1:7000` by default. The adapter accepts only loopback HTTP(S)
URLs, so it does not bypass the default external-egress policy. See
[OpenSERP local setup](docs/OPEN_SERP_LOCAL_SETUP.md) for the free installation
path and operating constraints.

### Offline GEO Checks

The `geo` category includes four deterministic adapters informed by the MIT
Geo Skills pack: `geo_citability`, `geo_llmstxt`, `geo_crawler_policy`, and
`geo_measurement`. They operate only on content supplied in the request and do
not claim to measure a live answer engine.

See [Adding Skills](docs/ADDING_SKILLS.md) for the complete directory,
manifest, test, security, and release contract.

### Scoring Formula

```
Score = (Relevance × 0.40) + (Cost × 0.25) + (Speed × 0.20) + (Track Record × 0.15)
```

Each factor is 0.0–1.0. Tools scoring ≥ 0.70 get dispatched. Multiple high-scoring tools get chained if chaining is cheaper or better than running them separately.

### Self-Evolution

Nerve-Center logs every dispatch outcome and periodically reviews its own performance:

- **Outcome Learning** — records success/failure of every tool dispatch
- **Self-Critique** — every 10 dispatches, reviews patterns and adjusts
- **Weight Adjustment** — rebalances scoring weights based on real outcomes
- **Rollback** — if an evolution makes things worse, reverts automatically

### Security

- Never sends user data to external services without consent
- Maximum chain depth of 5 (prevents runaway pipelines)
- Never auto-chains security tools with external APIs
- All data stays local by default

### Conflict Resolution

When chained tools produce contradictory instructions, a 6-level priority hierarchy resolves them automatically: Security > Legal > Performance > Semantics > SEO > Visual.

### Emergency Protocol

Five failure recovery modes — from chain failure through context overflow to cascade failure — each with automatic fallback and recovery. Nerve-center never crashes silently; it degrades gracefully and reports what happened.

---

## File Structure

```
nerve-center/
├── mcp_server.py                  # Local HTTP discovery and dispatch API
├── core/                           # Routing, scoring, chains, audit, registry
├── tools/                          # Self-describing local skill adapters
├── vault/                          # AES-GCM local secret store
├── cli/nervectl                    # Local command-line interface
├── docs/                           # Operations, security, and skill authoring
├── tests/                          # Offline unit and integration tests
├── SKILL.md                        # Agent routing protocol
└── README.md                       # This file
```

---

## For Other AI Agents

Nerve-Center is designed to be **readable by any LLM** that processes Markdown files. No proprietary formats, no binary dependencies.

**Integration:**
1. Place `nerve-center/` in your agent's skill directory
2. Read `SKILL.md` when a task arrives
3. Follow the 6-phase Core Protocol
4. Use `references/scoring-matrix.md` for scoring details
5. Append to `evolution-log.md` after each dispatch

---

## Examples

### Example 1: "Build me a landing page"
```
Intent: web frontend + content
Nerve-Center dispatches:
  1. skill-architect (structure)     → score: 0.82
  2. skill-web-master (HTML/CSS/JS)  → score: 0.91
  3. skill-seo-engine (meta + schema)→ score: 0.78
Chain cost: 0.85× individual = worth it
Result: complete, optimized landing page
```

### Example 2: "What's the latest on AI regulation in the EU?"
```
Intent: research
Nerve-Center dispatches:
  1. web_search (built-in)           → score: 0.84
No chain needed — single tool handles it.
```

### Example 3: "Analyze this CSV and make a presentation"
```
Intent: data + presentation
Nerve-Center dispatches:
  1. data:analyze (insights)         → score: 0.88
  2. pptx (presentation)            → score: 0.85
Chain: analyze → pptx
Result: data-driven slide deck
```

---

## Contributing

This is an open-source community tool. Contributions welcome:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear description

**Areas where help is needed:**
- Additional domain→tool mappings
- Scoring matrix calibration data
- Translations (SKILL.md is bilingual PL+EN)
- Integration guides for other AI agents

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

## Credits

Built by **EQinOX WEB MASTER TEAM #CODE**
Created by **TriglavK51 EQinOX**

Part of the EQinOX ecosystem — High Premium digital services built with clean, semantic, sustainable code.

---

*Nerve-Center v1.2.0 — September 2026*
