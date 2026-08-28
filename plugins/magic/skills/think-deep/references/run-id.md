# Run-id model — canonical rule for the `magic:think-*` family

The run-scoped protocol file `think-<id>.md` is named by its **id**. This is the single source of truth
for how that id is derived and minted. Every `magic:think-*` **executor** (think-deep and any sibling
mode) mints ids by this one rule; the `magic:think` **manager** reads these ids and never derives them.

## Id derivation + minting
A fresh run **mints** an id, checking the scratchpad once:
- **Candidate** = a **task slug** — lowercase the deliverable, drop stop-words, first ~4 significant
  tokens, hyphen-joined. For a **nested** run the candidate is the launcher's id + `-<k>` (`k` = next
  unused child number; it only *seeds* the candidate — the **minted id is authoritative**, never
  recompute a file's name from `<k>` later).
- **Uniqueness** — if `think-<candidate>.md` already exists, append a numeric suffix until free. **Every
  run gets a unique file** (top-level runs included — a re-run or same-slug task never overwrites a prior
  one).

## Filename + marker
- The id names the file `think-<id>.md` in the session scratchpad (never a hardcoded path).
- A live run leads every turn with the `[think] <id>` marker; the launch turn also announces the id.
- Nested runs each carry their own id; when a child returns, the parent resumes its own.

## Consumers
- `magic:think-deep` (executor) — **mints** per this rule on a fresh/nested run.
- `magic:think` (manager) — **reads** existing ids (filenames) / delegates minting to the executor; never
  derives an id itself.
- any future `magic:think-*` mode — mints per this rule, so the run-set stays uniform.
