# Scoring Matrix / Matryca Oceny Narzędzi

> Reference file for nerve-center SKILL.md — Phase 3: Scoring
> Plik referencyjny dla nerve-center — Faza 3: Ocena

---

## Formula / Wzór

```
SCORE = (Relevance × 0.40) + (Cost × 0.25) + (Speed × 0.20) + (Track_Record × 0.15)
```

Each factor is normalized to a 0.0–1.0 scale. Final score range: 0.0–1.0.

---

## Factor 1: RELEVANCE (weight: 0.40) / TRAFNOŚĆ

How well the tool's description matches the user's intent.

| Score | Meaning                                                    |
|-------|------------------------------------------------------------|
| 1.0   | Tool's description explicitly names this exact task type   |
| 0.8   | Strong semantic match — tool clearly handles this domain   |
| 0.6   | Partial match — tool covers part of the task               |
| 0.4   | Tangential — tool touches the domain but isn't primary     |
| 0.2   | Weak match — only keyword overlap, different actual use    |
| 0.0   | No match                                                   |

### How to assess relevance:
1. Extract keywords from user's request
2. Compare against tool's `description` field in frontmatter
3. Check `aliases` if available
4. Consider the tool's `trigger conditions` section
5. Penalize if tool's "DON'T use" section matches the current task

---

## Factor 2: COST (weight: 0.25) / KOSZT TOKENOWY

Estimated token consumption. Lower cost = higher score.

| Score | Estimated Token Usage | Typical Tool Type                    |
|-------|-----------------------|--------------------------------------|
| 1.0   | < 500 tokens          | Simple built-in (bash, view)         |
| 0.8   | 500–2,000 tokens      | Single-file skill, quick lookup      |
| 0.6   | 2,000–5,000 tokens    | Standard skill with references       |
| 0.4   | 5,000–15,000 tokens   | Complex skill with multiple phases   |
| 0.2   | 15,000–50,000 tokens  | Multi-tool chain, deep research      |
| 0.0   | > 50,000 tokens       | Massive pipeline, full audit         |

### How to estimate cost:
1. Count lines in the tool's SKILL.md (proxy for context consumption)
2. Check if tool loads reference files (adds to context)
3. Consider if tool spawns sub-processes or multi-step workflows
4. Factor in chain cost if combining with other tools

### Chain cost calculation:
```
chain_cost = sum(individual_costs) × 0.85
```
The 0.85 multiplier accounts for shared context between chained tools.
If `chain_cost > highest_single_tool_cost` AND quality gain < 15%,
prefer the single tool.

---

## Factor 3: SPEED (weight: 0.20) / SZYBKOŚĆ

How many steps/phases the tool requires to deliver results.

| Score | Steps to Completion | Example                              |
|-------|---------------------|--------------------------------------|
| 1.0   | 1 step              | Direct answer, single file read      |
| 0.8   | 2–3 steps           | Read skill + execute one action      |
| 0.6   | 4–5 steps           | Multi-phase workflow                 |
| 0.4   | 6–8 steps           | Complex pipeline with verification   |
| 0.2   | 9–12 steps          | Full audit with iteration            |
| 0.0   | > 12 steps          | Research + build + deploy + verify   |

### How to estimate speed:
1. Read the tool's protocol/workflow section
2. Count distinct phases or steps
3. Check if tool requires user input mid-flow (adds latency)
4. Factor in chain overhead (each chain link = +1 step)

---

## Factor 4: TRACK RECORD (weight: 0.15) / HISTORIA SUKCESU

How well this tool performed on similar tasks in the past.

| Score | Track Record                                              |
|-------|-----------------------------------------------------------|
| 1.0   | 5+ successful uses on similar tasks, no failures          |
| 0.8   | 3–4 successes, no failures                                |
| 0.6   | 1–2 successes, no failures (or new tool, no data yet)     |
| 0.4   | Mixed results — some successes, some partial outcomes     |
| 0.2   | More failures than successes on similar tasks             |
| 0.0   | Consistently fails or produces suboptimal results         |

### Default score for new/unknown tools: 0.6
New tools start at neutral. They earn their reputation through use.

### Where to find track record:
1. Check `evolution-log.md` for past dispatches
2. Look for `OUTCOME` entries matching the current task type
3. Weight recent entries more heavily than old ones

---

## Decision Thresholds / Progi decyzyjne

```
score >= 0.70  →  DISPATCH (tool is a strong fit)
score 0.50–0.69  →  CONSIDER (use if no better option exists)
score 0.30–0.49  →  WEAK (only use as chain support, never as lead)
score < 0.30  →  SKIP (tool is not relevant)
```

### Chain Decision Logic:
```
IF   top_tool.score >= 0.70
AND  second_tool.score >= 0.50
AND  chain_cost < top_tool_alone_cost × 1.15
AND  chain adds measurable quality improvement
THEN → CHAIN both tools

OTHERWISE → dispatch top_tool alone
```

---

## Competing Tools Resolution / Rozstrzyganie konkurencji

When multiple tools score similarly (within 0.05 of each other):

1. **Prefer specificity** — a tool built for exactly this task beats a general-purpose one
2. **Prefer simplicity** — fewer steps wins when scores are tied
3. **Prefer proven** — higher track record wins when relevance is tied
4. **Prefer local** — user skills > plugin skills > example skills (less context loading)

### Example: Web Research Task
```
nimble:search        → Relevance: 0.9, Cost: 0.4, Speed: 0.6, Track: 0.6 → 0.67
tavily:tavily-search → Relevance: 0.9, Cost: 0.6, Speed: 0.8, Track: 0.6 → 0.75
tinyfish:search      → Relevance: 0.9, Cost: 0.8, Speed: 0.8, Track: 0.6 → 0.81
web_search (built-in)→ Relevance: 0.7, Cost: 1.0, Speed: 1.0, Track: 0.8 → 0.84

Winner: built-in web_search (highest score due to zero extra cost + speed)
Unless: task requires depth that built-in can't provide → tinyfish:search
```

---

## Weight Adjustment Protocol / Protokół korekty wag

If evolution-log.md shows a pattern of suboptimal dispatches:

| Pattern Detected                        | Adjustment                        |
|-----------------------------------------|-----------------------------------|
| Right tool chosen but too expensive     | Cost weight: 0.25 → 0.30         |
| Wrong tool chosen despite good score    | Relevance weight: 0.40 → 0.45    |
| Chains consistently outperform singles  | Speed weight: 0.20 → 0.15        |
| New tools consistently underperform     | Track_Record weight: 0.15 → 0.20 |

**Constraint:** Weights must always sum to 1.00. Adjust in pairs (increase one, decrease another).

**Rollback:** If adjusted weights produce worse outcomes over 5 dispatches, revert to defaults:
`R=0.40, C=0.25, S=0.20, T=0.15`

---

*Scoring matrix v1.0 — part of nerve-center by TriglavK51 EQinOX (MIT License)*
