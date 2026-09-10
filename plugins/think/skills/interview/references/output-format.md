# Interview — state block + output doc (flush-left, console-safe)

Both blocks are **flush-left** markdown: one heading per field, values on their own lines, tags inline. Never
align columns, pad labels, or right-float — fixed-width layout deforms on console word-wrap and won't copy
without reflow.

## Live state block (hidden; rewritten after every answer)

Rewrite this before asking the next question. Keep answer summaries to ≤2 lines each. `show state` prints it.

```
## Interview state — after answer #N

### Meta
- Phase: recon | drill | crystallize
- Questions asked: N
- Active technique: 5-Whys | Scene | Devil's advocate | What-if-not | —
- Depth: shallow | mid | deep

### Grounding map (from Phase 0, immutable)
- Consensus: ...
- Open questions: ...
- Key data: ...
- Expert vs consensus: aligned | diverges on ...

### Question plan (mutates each answer)
1. ~~asked~~ → answer: <≤2-line summary>
2. next →
3. added after #N because ...

### Slot tracker
- core: filled | empty | partial — <gist>
- claim: ...
- counter: ...
- evidence: ...
- data: ...
- insight: ...
- so-what: ...

### Core sentence (current best)
"<one sentence>" — quality 1–10, missing: <stakes | specifics | surprise>

### Next move
- Technique: <which> · Question: <the actual next question> · Why: <the empty slot it targets>
```

## Output doc (emitted at close; skill-consumable)

Emit this as the last thing on the operator path, or return it to the calling skill. Every unfilled slot is
kept with an explicit flag so a downstream consumer knows what was not extracted.

```
# Interview material: <topic>
Date: <date> · Grounded: yes | no (no evidence reachable)

## Core
<the one sentence>

## Claim
<the expert's position, 2–3 sentences>

## Counter
<the strongest counter + the expert's rebuttal>

## Evidence
### Case 1: <name>
<concrete story with scene, specifics, timeline>

## Data
<numbers, sources, from the grounding map or the expert>

## Insight
<the non-obvious "thought X, found Y">

## So-what
<the actionable takeaway for a reader/consumer>

## Unfilled slots
- <slot>: not extracted — <why: expert couldn't reach it | out of scope | no evidence>
```
