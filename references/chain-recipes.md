# Chain Recipes / Przepisy na łańcuchy narzędzi

> Proven tool combinations for common task patterns.
> When nerve-center recognizes a pattern, it skips full scoring and dispatches
> the recipe directly — saving tokens and time.
>
> Sprawdzone kombinacje narzędzi dla typowych wzorców zadań.
> Gdy nerve-center rozpozna wzorzec, pomija pełny scoring i odpala przepis
> bezpośrednio — oszczędzając tokeny i czas.

---

## HOW RECIPES WORK / JAK DZIAŁAJĄ PRZEPISY

```
User request → Pattern match against recipes below
  ├── MATCH (confidence > 0.8) → dispatch recipe directly, skip Phase 2–3
  ├── PARTIAL MATCH (0.5–0.8) → use recipe as starting point, score remaining gaps
  └── NO MATCH → full scoring (Phase 1–6 as normal)
```

Recipe confidence = how many keywords from the trigger list appear in the user's request.
Formula: `confidence = matched_keywords / total_keywords × relevance_boost`

---

## RECIPE INDEX

### R01 — Build Landing Page / Zbuduj stronę
**Triggers:** "landing page", "strona", "zbuduj stronę", "website", "homepage"
**Chain:**
```
skill-architect (structure + tech decisions)
  → skill-web-master (semantic HTML/CSS/JS)
    → skill-seo-engine (meta, schema, headings)
      → skill-green-code (a11y + performance audit)
        → skill-security-ops (CSP, HTTPS, data safety)
```
**Token cost:** ~800 lines loaded (~5 skills × ~160 avg)
**When to break chain:** If page is internal (no SEO needed) → skip skill-seo-engine

---

### R02 — Full SEO Content / Treść SEO
**Triggers:** "content SEO", "artykuł", "blog post", "treść na stronę", "pozycjonowanie"
**Chain:**
```
skill-seo-engine (keyword strategy + brief)
  → skill-web-master (semantic markup)
    → skill-green-code (performance check)
```
**Token cost:** ~550 lines
**When to break chain:** If content is for social media (not web) → only skill-seo-engine

---

### R03 — Deploy to Production / Wdrożenie
**Triggers:** "deploy", "wdróż", "push", "production", "serwer", "hosting"
**Chain:**
```
skill-security-ops (pre-deploy security audit)
  → skill-deployment-ops (git + FTP + hosting config)
    → skill-green-code (final performance check)
```
**Token cost:** ~535 lines
**When to break chain:** If hotfix (urgent) → skip skill-green-code, go security → deploy

---

### R04 — New Project Setup / Nowy projekt
**Triggers:** "nowy projekt", "new project", "zacznij od zera", "setup", "inicjalizacja"
**Chain:**
```
skill-architect (tech stack + structure)
  → skill-security-ops (RODO + AI Act baseline)
    → skill-deployment-ops (repo + CI/CD setup)
      → skill-web-master (boilerplate code)
```
**Token cost:** ~730 lines
**When to break chain:** If project is backend-only → skip skill-web-master

---

### R05 — Skill Creation / Tworzenie skilla
**Triggers:** "stwórz skill", "nowy skill", "create skill", "skill-creator"
**Chain:**
```
skill-creator (example skill, structure)
  → skill-interop-guard (validate format)
    → skill-optimizer (quality benchmark)
```
**Token cost:** ~570 lines
**When to break chain:** If quick draft → only skill-creator

---

### R06 — Security Audit / Audyt bezpieczeństwa
**Triggers:** "audyt", "bezpieczeństwo", "RODO", "pentest", "security", "podatności"
**Chain:**
```
skill-security-ops (full OSINT + OPSEC + compliance)
  → skill-green-code (CSP headers + data handling)
    → skill-architect (architecture vulnerabilities)
```
**Token cost:** ~510 lines
**When to break chain:** If RODO-only → only skill-security-ops

---

### R07 — Code Review / Przegląd kodu
**Triggers:** "review", "przegląd kodu", "sprawdź kod", "code review", "refactor"
**Chain:**
```
skill-architect (architecture + patterns)
  → skill-green-code (a11y + performance + semantics)
    → skill-security-ops (security vulnerabilities)
```
**Token cost:** ~510 lines
**When to break chain:** If CSS-only review → only skill-green-code

---

### R08 — Research + Presentation / Badanie + prezentacja
**Triggers:** "zbadaj i zrób prezentację", "research + deck", "analiza + slajdy"
**Chain:**
```
web_search or tavily/nimble (research)
  → data:analyze (structure findings)
    → pptx (build presentation)
```
**Token cost:** ~700 lines (varies by research depth)
**When to break chain:** If research only → skip pptx

---

### R09 — Document Pipeline / Pipeline dokumentów
**Triggers:** "raport", "dokument", "report", "dokumentacja", "brief"
**Chain:**
```
data:analyze (if data-driven)
  → docx (Word document)
    → pdf (if PDF needed)
```
**Token cost:** ~500 lines
**When to break chain:** If markdown output OK → skip docx/pdf, write .md

---

### R10 — Skill System Health / Zdrowie systemu skilli
**Triggers:** "sprawdź skille", "skill audit", "stan systemu", "health check"
**Chain:**
```
skill-interop-guard (format validation)
  → skill-optimizer (quality scoring)
    → skill-evolution (update candidates)
      → nerve-center (update cost-database)
```
**Token cost:** ~740 lines
**When to break chain:** If single skill check → only skill-optimizer

---

## ADDING NEW RECIPES / DODAWANIE NOWYCH PRZEPISÓW

A recipe earns its place when:
1. The same chain is dispatched 3+ times with success
2. The chain is faster than individual scoring each time
3. The pattern is recognizable from 2–3 keywords

Format:
```
### RXX — Name / Nazwa PL
**Triggers:** "keyword1", "keyword2", ...
**Chain:** tool1 → tool2 → ...
**Token cost:** ~XXX lines
**When to break chain:** condition → shortened chain
```

Evolution: nerve-center auto-proposes new recipes in evolution-log.md
when it detects repeated successful chains.

---

*Chain Recipes v1.0 — part of nerve-center by TriglavK51 EQinOX (MIT License)*
