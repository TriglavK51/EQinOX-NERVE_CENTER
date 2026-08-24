# Cost Database / Baza kosztów tokenowych

> Real context-window cost of every skill, measured in lines loaded.
> Used by nerve-center Phase 3 (Scoring) for the Cost factor.
> Auto-generated from actual SKILL.md file sizes — not estimates.
>
> Realny koszt okna kontekstowego każdego skilla, mierzony w liniach.
> Używany przez nerve-center w Fazie 3 (Scoring) do czynnika Kosztu.
> Wygenerowany automatycznie z faktycznych rozmiarów plików SKILL.md.

---

## COST TIERS / POZIOMY KOSZTÓW

| Tier   | Lines     | Score | Context Impact                    |
|--------|-----------|-------|-----------------------------------|
| MICRO  | 1–50      | 1.0   | Negligible — always safe to load  |
| LIGHT  | 51–150    | 0.8   | Minimal — standard single skill   |
| MEDIUM | 151–300   | 0.6   | Moderate — full skill with refs   |
| HEAVY  | 301–500   | 0.4   | Significant — complex workflows   |
| ULTRA  | 501–999   | 0.2   | Major — loads substantial context |
| MEGA   | 1000+     | 0.1   | Critical — may fill context alone |

---

## USER SKILLS / SKILLE UŻYTKOWNIKA

| Skill                    | Lines | Tier   | Score | Has References |
|--------------------------|-------|--------|-------|----------------|
| nerve-center             | 275   | MEDIUM | 0.6   | YES (3 files)  |
| skill-interop-guard      | 204   | MEDIUM | 0.6   | NO             |
| skill-web-master         | 195   | MEDIUM | 0.6   | NO             |
| skill-cognitive-workflow | 195   | MEDIUM | 0.6   | NO             |
| skill-deployment-ops     | 192   | MEDIUM | 0.6   | NO             |
| skill-seo-engine         | 189   | MEDIUM | 0.6   | NO             |
| skill-security-ops       | 178   | MEDIUM | 0.6   | NO             |
| skill-guardian           | 176   | MEDIUM | 0.6   | NO             |
| skill-memory             | 171   | MEDIUM | 0.6   | NO             |
| skill-green-code         | 165   | MEDIUM | 0.6   | NO             |
| skill-architect          | 164   | MEDIUM | 0.6   | NO             |
| skill-persona-distiller  | 157   | MEDIUM | 0.6   | NO             |
| skill-fleet-manager      | 157   | MEDIUM | 0.6   | NO             |
| skill-handoff            | 154   | MEDIUM | 0.6   | NO             |
| skill-rules-engine       | 153   | MEDIUM | 0.6   | NO             |
| skill-orchestrator       | 149   | LIGHT  | 0.8   | NO             |
| skill-hunter             | 147   | LIGHT  | 0.8   | NO             |
| skill-optimizer          | 141   | LIGHT  | 0.8   | NO             |
| skill-video-analyst      | 135   | LIGHT  | 0.8   | NO             |
| skill-adapter            | 131   | LIGHT  | 0.8   | NO             |
| skill-evolution          | 122   | LIGHT  | 0.8   | NO             |
| tlumacz-terminala        | 71    | LIGHT  | 0.8   | NO             |
| aktualizacja-spolszczenia| 66    | LIGHT  | 0.8   | NO             |
| pomoc                    | 38    | MICRO  | 1.0   | NO             |
| slownik                  | 26    | MICRO  | 1.0   | NO             |

---

## PUBLIC SKILLS / SKILLE PUBLICZNE

| Skill              | Lines | Tier   | Score |
|--------------------|-------|--------|-------|
| file-reading       | 372   | HEAVY  | 0.4   |
| pdf                | 314   | HEAVY  | 0.4   |
| pdf-reading        | 308   | HEAVY  | 0.4   |
| pptx               | 238   | MEDIUM | 0.6   |
| xlsx               | 99    | LIGHT  | 0.8   |
| docx               | 91    | LIGHT  | 0.8   |
| product-self-knowledge | 65 | LIGHT  | 0.8   |
| frontend-design    | 55    | LIGHT  | 0.8   |

---

## PLUGIN SKILLS — TOP 30 HEAVIEST / NAJCIĘŻSZE WTYCZKI

| Skill                              | Lines | Tier  | Score |
|------------------------------------|-------|-------|-------|
| taste-skill:imagegen-frontend-mob  | 1465  | MEGA  | 0.1   |
| taste-skill:image-to-code          | 1228  | MEGA  | 0.1   |
| taste-skill:design-taste-frontend  | 1206  | MEGA  | 0.1   |
| daloopa:supply-chain               | 1147  | MEGA  | 0.1   |
| taste-skill:imagegen-frontend-web  | 987   | ULTRA | 0.2   |
| carta:carta-issuance               | 977   | ULTRA | 0.2   |
| data:build-dashboard               | 924   | ULTRA | 0.2   |
| sales:create-an-asset              | 867   | ULTRA | 0.2   |
| taste-skill:brandkit               | 798   | ULTRA | 0.2   |
| carta:carta-compensation-bench     | 794   | ULTRA | 0.2   |
| postiz:postiz                      | 707   | ULTRA | 0.2   |
| brightdata:scraper-builder         | 701   | ULTRA | 0.2   |
| adobe:adobe-batch-edit-photos      | 686   | ULTRA | 0.2   |
| adobe:adobe-retouch-portraits      | 658   | ULTRA | 0.2   |

> **Warning:** MEGA-tier skills consume 1000+ lines of context.
> Chain them only when absolutely necessary.
> Never load more than 1 MEGA skill in a single chain.

---

## CHAIN COST FORMULA / WZÓR KOSZTU ŁAŃCUCHA

```
chain_lines = sum(skill_lines for each skill in chain)
chain_cost_score = 1.0 - (chain_lines / 2000)  # normalized, capped at 0.0
chain_cost_score = max(0.0, chain_cost_score)

# Apply chain efficiency discount (shared context reduces overhead)
chain_cost_score = chain_cost_score × 1.10  # 10% bonus for chains
chain_cost_score = min(1.0, chain_cost_score)
```

### Example:
```
skill-architect (164) + skill-web-master (195) + skill-seo-engine (189)
chain_lines = 548
chain_cost_score = 1.0 - (548 / 2000) = 0.726
with discount: 0.726 × 1.10 = 0.799 → Cost Score: 0.80
```

---

## REFRESH PROTOCOL / PROTOKÓŁ ODŚWIEŻANIA

This database should be regenerated when:
1. New skills are installed
2. Existing skills are significantly edited (±30 lines)
3. nerve-center detects a cost prediction miss >0.2

Regeneration command (for evolution-log):
```
find /mnt/skills -name "SKILL.md" -exec wc -l {} \; | sort -rn
```

---

*Cost Database v1.0 — generated 2026-08-23 — part of nerve-center by TriglavK51 EQinOX (MIT License)*
