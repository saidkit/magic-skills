# Render forms — projecting a pinned contract into portable prose

critic's Phase 3 can **render** the already-pinned `Done-when` as a human-readable prompt for
future composition (hand to a teammate, paste into a fresh session, file as a reusable bar). This
is a **projection of the pinned contract, never authored from prose** — the discipline was applied
at authoring; terseness is only a rendering choice. Default is **terse**; `as full prompt` spells
out the standard for a zero-context reader.

## Terse (default) — the floor pointer + the bar + the stop

Keep three beats: **what**, the **sharp standard** (name the file, trust the reader to open it),
the **stop**. Drop the enumeration — a human infers it.

**T target (objective / conformance) — e.g. a generated spec corpus:**
```
critic · <target> → T (spec-conformance)
floor: <cheap deterministic checks — counts · ids resolve · collisions clean>
bar:   each unit obeys <STANDARD-FILE> (<the 3–4 load-bearing rules>); <cross-ref
       resolution>; adversarial per unit, hardest on <the money/data paths>; dead
       forms (<forbidden strings>) never asserted as current — read, don't grep.
stop:  two passes turn up nothing new.
```

**C target (subjective / perceptual) — the classic three-slot (Task · Build · Bar):**
```
Make <deliverable> as good as <anchor>.
Build: <how — fan out, each paired with a harsh critic, one item at a time>.
Bar:   judge it BLIND against <reference>, whole artifact — pass at ≥K/N looks.
       Stop there; don't gild.
```

## Full (`as full prompt`) — enumerated, for a zero-context reader

Same three beats, but the **standard is spelled out** (the reconciliations, the id rules, the
forbidden forms) so a reader with none of the project's context can execute it without opening
another file. Use when handing off outside the team. (This is the long form — it reads like a
job spec because it carries what the terse form points at.)

## Rules for any render

- **Never invent the bar in prose.** Render only what Phase 1/2 pinned; if a beat is missing,
  the contract is incomplete — go back, don't paper over it in prose.
- **Terse points, full enumerates** — same contract, two audiences (a teammate who can open the
  standard file · a stranger who can't).
- **The stop is non-negotiable in both** — a rendered prompt without a bounded stop is the
  absolute-score non-termination trap the whole skill exists to prevent.
- **A render is an export, not a run** — emitting prose is a terminal exit (`as prompt`), never a
  substitute for driving the contract through the loop.
