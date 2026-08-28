# ideate — output format (console-safe)

Emit the result as **flush-left markdown**. The reader copies it straight from a terminal, so it must survive console word-wrap with **no reflow**. That rules out fixed-width layout:

- **One `###` heading per field** — value on the next line, flush-left. Never `Problem:      …   Rubric:` aligned to a column (the padding breaks on wrap).
- **The Field is a flush-left `-` bullet per idea**, each tagged by its lens (`- [contrarian] <idea>`). Never a padded `Field:` block with hanging indents.
- **Top-N is a flush-left numbered list** — `1. <idea> — survives: … · risk: …`; let long survives/risk text wrap naturally.
- **No manual line-breaks inside a value** — write prose; the console wraps it.

## Template — fill in and emit exactly this shape

### Problem
<the problem in one line>

### Rubric
<axis · axis · axis>   ·   N = <k>

### Field
<k ideas — pruned <m> near-duplicates>
- [<lens>] <idea>
- [<lens>] <idea>
- …

### Top <N>
1. <idea> — survives: <rubric fit> · risk: <main weakness>
2. <idea> — survives: … · risk: …
3. <idea> — survives: … · risk: …

### Usage
→ run it: think!/auror! <idea> · build to a bar: gauntlet! <idea> · sharpen first: smart! <idea>
