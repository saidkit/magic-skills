# Probe record — the experiment's mechanical evidence file

Write it under the feature's working directory (for example `docs/working/PROJ-01/probe-<topic>.md`; where the
project has none, a `probe-<topic>.md` beside the code) so a later sweep finds it and the brief can cite a path. It
must let a reader **recompute** the table, not take it on trust.

## Required shape
A `results:` line (or a `## Results` heading) followed by one line per **arm × case**:

```
results:
<arm> <case> PASS
<arm> <case> FAIL <what went wrong>
```

- **Every arm on every case** — a partial table cannot compare.
- **The negative control is a row** — a case built so a broken / over-permissive arm PASSES when it should FAIL.
  Name it in the record so a reader sees the battery can detect a false pass.
- **Real output, mechanically captured** — the verdicts come from running the real engine and redirecting its
  output, never hand-typed. Keep the command (or script) beside the table so it re-runs.
- **One row per verdict** — do not give the same arm × case two different verdicts; a record that contradicts
  itself is not evidence.

## What the brief cites
The `### experiment` field names this file plus "arms × cases, negative control named". The `### finding` field
states what the table showed mechanically; `### conclusion` states what that licenses, checked against the
step-1 criteria — a true finding can still carry a wrong inference.

## A G1 one-check needs no such file
One cheap check of the single pivotal claim, reported in the `### experiment` field as
`one-check: <command or path> — <result>`. Over-investing a G0/G1 question into a battery is the same failure as
guessing on an empirical one.
