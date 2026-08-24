# Nerve-Center Evolution Log / Dziennik Ewolucji

> This file is the memory of nerve-center. Every dispatch, every outcome,
> every lesson learned is recorded here. This enables self-evolution,
> self-critique, and rollback when needed.
>
> Ten plik to pamięć nerve-center. Każde uruchomienie, każdy wynik,
> każda wyciągnięta lekcja jest tu zapisana. To umożliwia samoewolucję,
> autokrytykę i cofnięcie zmian gdy trzeba.

---

## FORMAT

Each entry follows this structure:
```
### [DATE] | [DISPATCH_ID]
- **Task type:** [code/content/data/deploy/research/design/security/other]
- **User intent:** [1-line summary of what the user asked]
- **Tools dispatched:** [tool1] → [tool2] → ... (or single tool)
- **Scores:** [tool1: X.XX, tool2: X.XX, ...]
- **Chain used:** yes/no
- **Outcome:** success / partial / failure
- **Lesson:** [1 sentence — what to remember for next time]
- **Tags:** [DISPATCH] / [EVOLUTION] / [ROLLBACK] / [GAP] / [SELF-CRITIQUE]
```

---

## EVOLUTION SNAPSHOTS / MIGAWKI EWOLUCJI

Before any self-evolution modifies SKILL.md, the changed section is
snapshot here. This enables rollback.

```
### [SNAPSHOT] [DATE] | Version X.X.X → X.X.Y
- **Section changed:** [which part of SKILL.md was modified]
- **Previous content:**
  > [exact text that was replaced]
- **New content:**
  > [exact text that replaced it]
- **Reason:** [why the change was made]
- **Triggered by:** [which log entries caused this evolution]
```

---

## SELF-CRITIQUE SCHEDULE / HARMONOGRAM AUTOKRYTYKI

Self-critique triggers:
- After every 10 `[DISPATCH]` entries
- After any `[FAILURE]` outcome
- When the same tool is dispatched 5+ times in a row (over-reliance signal)

Self-critique format:
```
### [SELF-CRITIQUE] [DATE]
- **Entries reviewed:** [DISPATCH_ID range]
- **Patterns found:**
  - [pattern 1]
  - [pattern 2]
- **Action taken:** [adjustment / no change / evolution triggered]
- **Weight adjustments:** [if any — see scoring-matrix.md]
```

---

## LOG ENTRIES

*— Log starts below this line. Entries are appended chronologically. —*

---

### 2026-08-23 | INIT-001
- **Task type:** system
- **User intent:** Skill creation — nerve-center initialized
- **Tools dispatched:** skill-creator (manual)
- **Scores:** N/A (initial setup)
- **Chain used:** no
- **Outcome:** success
- **Lesson:** First entry. Scoring matrix set to default weights (R=0.40, C=0.25, S=0.20, T=0.15). All tools start with track_record=0.6.
- **Tags:** [DISPATCH] [EVOLUTION]
