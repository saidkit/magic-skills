---
name: lumos
description: |
  precedent/decision-record search. When to use: At the start of any `§D` walk, multi-question decision pass, or `scope.md` review; Before walking an agent-produced scope / decision-map / framing with the operator; When the operator asks "is this consistent with prior decisions?" or "did we decide this before?"; When you notice yourself about to propose a default without consulting precedent — STOP, run `lumos`, then propose.; When you notice the same type of question surfacing repeatedly across sessions (the meta-failure signal — precedent exists but isn't reachable from your usual research path).
---

# Precedent/decision-record search

Before proposing defaults, accepting a spawned-agent's framing, or answering "what's the default for X", EXHAUST the precedent search across the project's decision record. Five sources, in order:

1. **`CLAUDE.md`** (project + user-global) — grep for the question's core concepts. Project invariants live here; user-global macros and standing preferences live here. If the project uses R-rule labels (`R-ENGINE-CLONE`, `R-DEV-TOKEN`, etc.) — grep those too; they're the project's shorthand for cross-cutting invariants and surface in ADR headings + scope.md citations + code comments.
2. **Memory files** — grep `MEMORY.md` index + every `<name>.md` in this project's memory directory. Prior-session feedback, project decisions, references.
3. **ADRs** (or whatever the project's decision-log directory is — `docs/adr/`, `decision-log/`, `architecture/decisions/`, etc.) — grep every file for the question's core concepts. Don't trust an agent's citation chain alone; the agent may have surfaced one ADR but missed a contradicting one.
4. **Prior-feature working dirs** (`docs/working/INIT-*/scope*.md`, `docs/working/FEAT-*/scope*.md`, `*/debrief.md`, `*/accept-*.md`, or project equivalents) — grep for the same concepts. Reuses across features signal precedent; reversals in debriefs signal "scope-time default was wrong."
5. **Prior probe / wire-capture records** (scope.md §A blocks, `wip*.md` files) — for probe-mode / live-system outcomes that the current question depends on. Workarounds (dev tokens, fixture endpoints, env overrides) live here, not in ADRs.

**Output:** List what was found per source, with citations. Then:
- If precedent EXISTS → default to it; cite the source; surface conflicts between precedent and the current proposal (especially agent-produced ones) as the FIRST thing in your output.
- If precedent DOES NOT exist → name the gap explicitly; propose a default grounded in adjacent precedents (similar features, related ADRs) AND surface the gap as something the project may want to codify (e.g., as a new ADR or memory entry).

**Purpose.** Counteracts two recurring failure modes:
- **Agent-output-bias** — treating spawned-agent framings (scope-refine, code-explorer, code-architect, etc.) as authoritative without independent cross-check. The agent did its own research; that doesn't exempt you from re-grounding it.
- **Convenience-default bias** — proposing the easier-to-implement answer instead of the architecturally-coherent one. Precedent often points to the harder-but-correct path; convenience defaults skip past it.

Both lead to the SAME smell: questions getting re-litigated each session, with the operator forced to manually re-surface decisions that the decision-record already contains.

**When to use:**
- At the start of any `§D` walk, multi-question decision pass, or `scope.md` review.
- Before walking an agent-produced scope / decision-map / framing with the operator.
- When the operator asks "is this consistent with prior decisions?" or "did we decide this before?".
- When you notice yourself about to propose a default without consulting precedent — STOP, run `lumos`, then propose.
- When you notice the same type of question surfacing repeatedly across sessions (the meta-failure signal — precedent exists but isn't reachable from your usual research path).

**Cross-project applicability.** The 5-step procedure is project-agnostic. Each project's "precedent locations" differ (ADR-* vs decision-log vs RFCs; `docs/working/` vs `notes/` vs `planning/`); the macro adapts to whatever directory layout the project uses. The principle holds: don't propose a default without first checking what the project has already decided. If a project doesn't have a decision record at all, `lumos` surfaces that as the first finding ("no decision record found — proposing without precedent").

**Does NOT carry across invocations.** Each `lumos!` triggers a fresh sweep for the current question; it doesn't make subsequent answers in the session "automatically precedent-checked".
