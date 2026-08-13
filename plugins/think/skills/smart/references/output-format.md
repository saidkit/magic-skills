# smart — output format (console-safe)

Emit the sharpened goal as **flush-left markdown**. The reader copies it straight out of a terminal, so it must survive console word-wrap with **no reflow or manual editing**. That rules out anything fixed-width:

- **One `###` heading per field** — the value starts on the next line, flush-left. Never `Field:      <value>` aligned to a column (the padding + hanging-indent continuation is what breaks on wrap).
- **Tags inline, as a lead-in** — `Measurable (the gate's raw material) [✓]:` then the point(s). Never right-float `[Measurable ✓]` to the end of a line with padding — that padding collapses on wrap.
- **Multi-point fields → flush-left `-` bullets.** Never `•` with a hanging indent aligned under a value.
- **No manual line-breaks inside a value** — write natural prose and let the console wrap it. Fixed-width alignment plus hard-wraps is exactly what deforms.

## Template — fill in and emit exactly this shape

### Goal (sharpened)
<the goal's IFR — one line>

### Objective
<one specific, decomposable target>

### In scope
<what's included>

### Out of scope
<what's excluded>

### Success signal
Measurable (the gate's raw material) [✓]:
- <a signal a gate can evaluate — vs a baseline / a threshold / a count>

### Stops when
Convergent [✓]:
- <reachable termination — "done when the signal holds", not "perfect">

### Watch-outs
- <Achievable / Relevant / feasibility flags, if any>

### Usage
→ run it: think! <goal> · auror! <goal>   (quality target? pin the bar first: critic! <goal>)

Then a one-line close: `STOP — goal shaped (Measurable + Convergent); no Done-when authored, nothing built.` (standalone MAY offer to drive it with think! on confirm).
