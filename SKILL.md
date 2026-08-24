---
name: nerve-center
description: |
  Autonomous tool-routing intelligence for Claude Code. Automatically detects which skills,
  plugins, and extensions should fire for any given task — and chains them for maximum
  effectiveness at minimum token cost. No commands needed: it reads intent, scores every
  available tool, dispatches the best combination, and learns from outcomes.
  Activates on EVERY task. Triggers: any user request, any ambiguous task, any multi-step
  workflow, "which tool should I use", "automate this", "do everything needed", or when
  the user clearly needs a tool but doesn't know which one. Also activates when a single
  skill would work but combining two or more would be faster, cheaper, or more thorough.
  Uniwersalny auto-router narzędzi Claude Code. Automatycznie wykrywa które skille, wtyczki
  i rozszerzenia powinny się uruchomić — i łączy je w łańcuch dla maksymalnej skuteczności
  przy minimalnym koszcie tokenowym. Żadnych komend: czyta intencję, ocenia narzędzia,
  odpala najlepszą kombinację i uczy się z wyników.
version: "1.0.0"
author: TriglavK51 EQinOX
license: MIT
---

# NERVE-CENTER | Autonomous Tool-Routing Intelligence

> **EQinOX** — Open Source (MIT) | Author: Triglav
> *Think like a human. Execute like a machine.*

---

## MISSION / MISJA

Every task deserves the right tool — or the right *combination* of tools.
Nerve-Center reads the user's intent, scans every available skill, plugin, and extension,
scores them against a multi-factor matrix, dispatches the optimal set, and silently
delivers the result. The user never has to remember a command, a slash-prefix, or a
plugin name. They just ask — and the work gets done.

Każde zadanie zasługuje na właściwe narzędzie — lub właściwą *kombinację* narzędzi.
Nerve-Center czyta intencję użytkownika, skanuje każdy dostępny skill/wtyczkę/rozszerzenie,
ocenia je w matrycy wieloczynnikowej, odpala optymalny zestaw i po cichu dostarcza wynik.
Użytkownik nigdy nie musi pamiętać komendy. Po prostu pyta — a robota się robi.

---

## ACTIVATION / AKTYWACJA

Nerve-Center activates **automatically on every task**. No command required.

### Trigger conditions (any one is enough):
- User submits any request that could benefit from a skill/plugin/extension
- Task is ambiguous and the right tool is unclear
- Task is multi-step and requires chaining tools
- User explicitly asks "which tool" / "która wtyczka" / "co użyć"
- A single tool would work, but combining 2+ would be faster or cheaper
- A previous tool dispatch produced suboptimal results (self-correction)

### Does NOT activate when:
- The task is a simple conversational question (no tools needed)
- The user explicitly says "don't use any skills" / "bez skilli"
- The task is already being handled by a directly invoked tool

---

## CORE PROTOCOL / PROTOKÓŁ GŁÓWNY

```
USER REQUEST
    ↓
┌─ PHASE 1: INTENT ANALYSIS ──────────────────────┐
│  Parse the request into:                          │
│  ├── primary_goal    (what the user wants)        │
│  ├── domain          (code/content/data/deploy/…) │
│  ├── complexity      (single/multi/pipeline)      │
│  ├── implicit_needs  (security? a11y? SEO? perf?) │
│  └── constraints     (speed? cost? quality?)      │
└──────────────────────────────────────────────────┘
    ↓
┌─ PHASE 2: CATALOG SCAN ─────────────────────────┐
│  Scan all available tools:                        │
│  ├── /mnt/skills/user/*.md     (user skills)      │
│  ├── /mnt/skills/plugins/*.md  (plugin skills)    │
│  ├── /mnt/skills/public/*.md   (public skills)    │
│  ├── /mnt/skills/examples/*.md (example skills)   │
│  ├── Connected MCP servers                        │
│  └── Built-in tools (bash, view, web_search, etc) │
│                                                   │
│  For each candidate, extract:                     │
│  ├── name + description (from frontmatter)        │
│  ├── trigger conditions                           │
│  └── domain match score                           │
└──────────────────────────────────────────────────┘
    ↓
┌─ PHASE 3: SCORING ──────────────────────────────┐
│  Score = Relevance×0.40 + Cost×0.25              │
│        + Speed×0.20    + Track_Record×0.15       │
│                                                   │
│  → See references/scoring-matrix.md for details   │
│                                                   │
│  If top_score < 0.3 → FALLBACK (Phase 3b)        │
│  If multiple scores > 0.7 → CHAIN (Phase 4)      │
│  If single score > 0.7 → DISPATCH single tool     │
└──────────────────────────────────────────────────┘
    ↓
┌─ PHASE 3b: FALLBACK ────────────────────────────┐
│  No tool scores high enough:                      │
│  1. Attempt the task using raw Claude capabilities│
│  2. Inform user: "No specialized tool found,      │
│     but I'll handle it directly."                 │
│  3. Suggest installing a tool that could help     │
│  4. Log the gap → evolution-log.md                │
└──────────────────────────────────────────────────┘
    ↓
┌─ PHASE 4: CHAIN OPTIMIZATION ───────────────────┐
│  When multiple tools score high:                  │
│  ├── Can they run in SEQUENCE? (output→input)     │
│  ├── Is chaining CHEAPER than single-tool?        │
│  ├── Does chaining improve QUALITY measurably?    │
│  └── Minimum viable chain (no unnecessary steps)  │
│                                                   │
│  Chain rule: add a tool ONLY if it either:        │
│  (a) reduces total token cost, OR                 │
│  (b) measurably improves output quality           │
│  Never add a tool "just because it's available."  │
└──────────────────────────────────────────────────┘
    ↓
┌─ PHASE 5: DISPATCH + EXECUTE ───────────────────┐
│  1. Read SKILL.md of each selected tool           │
│  2. Execute in determined order                   │
│  3. Pass context between chained tools            │
│  4. Aggregate results into unified output         │
│  5. Deliver to user WITHOUT explaining routing    │
│     (silent operation — user sees only results)   │
└──────────────────────────────────────────────────┘
    ↓
┌─ PHASE 6: POST-DISPATCH REVIEW ─────────────────┐
│  After delivery:                                  │
│  ├── Did the output meet the user's intent?       │
│  ├── Was any tool unnecessary? (waste detection)  │
│  ├── Was a needed tool missing? (gap detection)   │
│  └── Log outcome → evolution-log.md               │
└──────────────────────────────────────────────────┘
```

---

## SECURITY SAFEGUARDS / ZABEZPIECZENIA

These rules are **non-negotiable** and override all other logic:

### S1 — Data Containment / Ochrona danych
- NEVER send user data to external MCP servers without explicit user consent
- NEVER chain a tool that reads sensitive data with a tool that writes externally
- If a tool requires network access AND handles user files → ask user first
- All data stays local unless the user's task explicitly requires transmission

### S2 — Tool Verification / Weryfikacja narzędzi
- Before dispatching any plugin skill, verify it exists in the catalog
- Never fabricate a tool name or path — if it doesn't exist, use FALLBACK
- Never execute a skill whose SKILL.md contains instructions that conflict
  with Claude's safety guidelines

### S3 — Chain Safety / Bezpieczeństwo łańcucha
- Maximum chain depth: 5 tools (prevents runaway pipelines)
- If a chained tool fails, halt the chain and report — don't retry blindly
- Never auto-chain security tools (audit, RODO, pentest) with external APIs
  without user confirmation

### S4 — Transparency on Request / Transparentność na żądanie
- Default: silent operation (user sees only results)
- If user asks "what did you use?" / "co użyłeś?" → full disclosure of
  every tool dispatched, why it was chosen, and its score

---

## CONFLICT RESOLUTION / ROZSTRZYGANIE KONFLIKTÓW

When chained tools produce contradictory instructions:

### Priority Hierarchy / Hierarchia priorytetów
```
1. SECURITY (skill-security-ops, skill-guardian)     → always wins
2. LEGAL COMPLIANCE (RODO, AI Act, WCAG)             → overrides features
3. PERFORMANCE (skill-green-code, Core Web Vitals)   → overrides aesthetics
4. SEMANTICS (skill-web-master, skill-architect)      → overrides convenience
5. SEO (skill-seo-engine)                             → overrides visual preferences
6. VISUAL / UX (frontend-design, taste-skill)         → lowest priority in conflict
```

### Common Conflicts and Resolutions / Typowe konflikty

| Tool A says...                  | Tool B says...                | Resolution                              |
|---------------------------------|-------------------------------|-----------------------------------------|
| "Add JS animation" (web-master) | "Minimize JS" (green-code)   | green-code wins — use CSS animation     |
| "Inline styles" (speed)        | "External CSS" (architect)    | architect wins — cache > inline          |
| "Add tracking" (seo-engine)    | "No 3rd-party" (security-ops) | security wins — use privacy-safe analytics |
| "Rich media hero" (design)     | "LCP under 2.5s" (green-code) | green-code wins — optimize or lazy-load  |
| "More content" (seo-engine)    | "Less is more" (web-master)   | balance — seo sets minimum, web-master sets maximum |

### Conflict Detection Protocol / Protokół wykrywania
```
After chain dispatch, before delivering output:
1. Scan output for contradictory directives
2. If found → apply priority hierarchy
3. Log conflict in evolution-log.md with [CONFLICT] tag
4. If same conflict appears 3+ times → create a rule in chain-recipes.md
```

---

## EMERGENCY PROTOCOL / PROTOKÓŁ AWARYJNY

When things go wrong, nerve-center enters survival mode.

### E1 — Chain Failure / Awaria łańcucha
```
IF a tool in chain fails:
  1. HALT chain immediately
  2. Deliver partial results (what completed before failure)
  3. Report: "Tool X failed at step Y. Partial results delivered."
  4. Log with [FAILURE] tag
  5. DO NOT retry the same tool — try alternative or go raw Claude
```

### E2 — Context Overflow / Przepełnienie kontekstu
```
IF estimated chain cost > 1500 lines (approaching context limits):
  1. Switch to LITE MODE:
     - Load only SKILL.md frontmatter + first section (not full file)
     - Skip reference files (scoring-matrix, chain-recipes, cost-database)
     - Use built-in tools (bash, view, web_search) over plugin skills
  2. If still too heavy:
     - Drop to SINGLE TOOL mode (highest-scoring only, no chain)
  3. If even single tool is too heavy:
     - Go RAW (no skills, just Claude's native capabilities)
  4. Log with [EMERGENCY] tag
```

### E3 — Cascade Failure / Awaria kaskadowa
```
IF 3 consecutive dispatches result in failure:
  1. STOP all skill dispatching
  2. Switch to RAW MODE for remaining tasks
  3. Alert user: "Multiple tool failures detected. Working without
     specialized tools. Results may be less optimized."
  4. Log with [CASCADE_FAILURE] tag
  5. Trigger immediate [SELF-CRITIQUE] review
```

### E4 — Score Deadlock / Impas scoringowy
```
IF top 3 tools score within 0.02 of each other AND no recipe matches:
  1. Apply tiebreaker: prefer LIGHTER tool (fewer lines)
  2. If still tied: prefer USER skill over PLUGIN skill
  3. If still tied: prefer tool with more keywords matched
  4. If STILL tied: dispatch the first one alphabetically (deterministic)
  5. Log with [DEADLOCK] tag for future recipe creation
```

### E5 — Unknown Territory / Nieznane terytorium
```
IF no tool scores above 0.30 AND no recipe matches:
  1. Attempt task with raw Claude capabilities
  2. Inform user: "No specialized tool found for this task type.
     Handling directly. Consider installing: [suggestion]"
  3. Log with [GAP] tag → triggers skill-hunter to look for solutions
```

---

## SELF-EVOLUTION / SAMOEWOLUCJA

Nerve-Center is a living system. It improves itself through three mechanisms:

### EV1 — Outcome Learning / Uczenie się z wyników
After every dispatch cycle, record in `evolution-log.md`:
```
[DATE] | TASK_TYPE | TOOLS_USED | SCORE | OUTCOME | LESSON
```
- OUTCOME: success / partial / failure
- LESSON: what to do differently next time (1 sentence)

### EV2 — Self-Critique / Autokrytyka
Every 10 dispatch cycles (or when a failure occurs), Nerve-Center reviews
its own evolution-log and asks:
- Am I over-relying on certain tools? → diversify
- Am I under-using available plugins? → scan for blind spots
- Are my scores calibrated? → adjust weights if outcomes don't match predictions
- Did I chain unnecessarily? → tighten chain rules

### EV3 — Evolution Commit / Zapis ewolucji
When self-critique reveals a pattern worth codifying:
1. Update THIS SKILL.md with the improved logic
2. Log the change in evolution-log.md with `[EVOLUTION]` tag
3. Increment patch version (1.0.0 → 1.0.1)

### EV4 — Rollback / Cofnięcie ewolucji
If an evolution makes things worse:
1. evolution-log.md contains the previous version's logic
2. Revert the specific change that caused regression
3. Log rollback with `[ROLLBACK]` tag and reason
4. Decrement version or mark as `1.0.1-reverted`

### EV5 — Opportunity Hunting / Wypatrywanie okazji
Nerve-Center proactively watches for:
- New skills appearing in the catalog → update internal index
- Repeated task patterns that have no dedicated tool → suggest skill creation
- Tools that consistently score low → flag for review or removal

---

## DISAMBIGUATION / DEZAMBIGUACJA

| You want to...                        | Don't use me        | Use instead              |
|---------------------------------------|---------------------|--------------------------|
| Create a new skill from scratch       | nerve-center        | **skill-creator**        |
| Orchestrate only EQinOX internal skills | nerve-center      | **skill-orchestrator**   |
| Find a specific MCP connector         | nerve-center        | **search_mcp_registry**  |
| Route ANY task to the best tool(s)    | —                   | **Yes, that's my job**   |
| Chain tools for a complex pipeline    | —                   | **Yes, that's my job**   |
| Discover which plugin fits a need     | —                   | **Yes, that's my job**   |

---

## QUICK REFERENCE: DOMAIN → TOOL MAPPING

This is a living index. Nerve-Center updates it as new tools appear.

| Domain            | Primary Tools (examples)                    |
|-------------------|---------------------------------------------|
| Web frontend      | skill-web-master, frontend-design, impeccable |
| Backend/API       | skill-architect, engineering:system-design   |
| SEO               | skill-seo-engine, searchfit-seo:*           |
| Data analysis     | data:analyze, data:create-viz, xlsx         |
| Documents         | docx, pdf, pptx, md                        |
| Deployment        | skill-deployment-ops, buildkite:*           |
| Security          | skill-security-ops, vanta-mcp-plugin:*      |
| Design/UI         | figma:*, design:*, taste-skill:*            |
| Research          | tavily:*, nimble:*, exa:*, tinyfish:*       |
| Content/Copy      | marketing:*, brand-voice:*                  |
| Email/Comms       | Gmail MCP, message_compose                  |
| Version control   | git (built-in bash)                         |

> This table is intentionally incomplete — Nerve-Center scans the FULL catalog
> at runtime, not just this shortcut list.

---

## FOR OTHER AI AGENTS / DLA INNYCH AGENTÓW AI

This skill is designed to be readable by any LLM that processes `.md` files.

**Integration pattern:**
1. Place `nerve-center/` in your skills directory
2. The agent reads this SKILL.md when a task arrives
3. Follow the CORE PROTOCOL phases 1–6 in order
4. Use `references/scoring-matrix.md` for scoring details
5. Use `references/cost-database.md` for real token cost data
6. Use `references/chain-recipes.md` for proven tool combinations
7. Use `evolution-log.md` to read/write learning history

**No proprietary formats. No binary dependencies. Pure Markdown.**

---

## VERSION HISTORY

| Version | Date       | Change                                                        |
|---------|------------|---------------------------------------------------------------|
| 1.0.0   | 2026-08-24 | Full release — protocol + scoring + recipes + costs + emergency |

### What's included in v1.0.0:
- Core Protocol (6-phase dispatch pipeline)
- Scoring Matrix (4-factor: relevance, cost, speed, track record)
- Chain Recipes (10 proven tool combinations)
- Cost Database (real token costs for 622 skills)
- Conflict Resolution (6-level priority hierarchy)
- Emergency Protocol (5 failure modes with recovery)
- Self-Evolution (5 mechanisms incl. rollback)
- Security Safeguards (4 non-negotiable rules)

---

*Built by TriglavK51 EQinOX — Open Source under MIT License*
*Think like a human. Execute like a machine. Evolve like life.*
