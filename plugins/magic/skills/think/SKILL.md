---
name: think
description: >
  Run-manager for magic:think-deep — observe, resume, clean up, and move the run-scoped
  think-<id>.md protocol files think-deep writes to the session scratchpad. The manager to
  think-deep's executor. Verbs: list · status · clear · resume · export · continue.
  Activates ONLY on "/magic:think <verb>" or "think!! <verb>" where <verb> ∈ list|status|clear|resume|export|continue is the operative token — alone, or with a lone operand (all · an id · a path) — AND NOTHING ELSE. NOT for task execution: a verb followed by a free-form task phrase (e.g. "think!! clear up the spec") runs magic:think-deep.
---

# Think — magic:think-deep run manager

Manage the `think-<id>.md` protocol files `magic:think-deep` writes to the session scratchpad: see the
run-set, resume a run, clean up, and bridge one across sessions.

## Contract — holds every verb
- **Compose, never fork.** READ think-deep's run model — the run-id derivation, the `[think] <id>` marker,
  the live-leaf rule, the `Parent:`/`Closed:` headers (`magic:think-deep` owns them in its SKILL.md); never
  redefine or reimplement it. `resume`/`continue` hand off to `Skill(magic:think-deep)`; never duplicate its
  reconstruct-from-disk logic. Never edit think-deep.
- **Read-mostly.** `list`/`status` never mutate; `clear` (delete), `export` (copy), `continue`
  (re-enter external) are the only writers.
- **Manager-only.** Never execute a think task. A verb routes here only as the **operative token** (bare, or
  + a lone `all`/id/path); a verb followed by a task phrase (`clear up the spec`) is the executor's.
- **Scratchpad-scoped.** `list`/`status`/`clear`/`resume` operate on the current session scratchpad only;
  durable dirs are touched only by `export`/`continue`.
- **Run id.** A run is named by its **id** — the `think-<id>.md` stem, carried as the `[think] <id>` marker.
  The canonical id rule is `magic:think-deep`'s `references/run-id.md` (the single source for the
  `magic:think-*` family). `list`/`status`/`resume`/`export` read **existing** ids (filenames); `continue`
  gets a fresh id by handing off to `magic:think-deep`, which mints it — `magic:think` never derives an id,
  no forked id scheme.
- **Closure** (`magic:think-deep`'s rule, restated for reference; never redefine) = the run's Gate-log verdict line (`all PASS` / `escalated`): a run with one is terminal (closed); its `Closed:` header is a mirror that may lag, never the source when a verdict line exists. Legacy shape: a file with `Closed: done|escalated` and no Gate-log verdict line was written by an older version and is terminal too. "Un-closed" below means: no verdict line and `Closed: no`.
- **Live leaf** = the un-closed run no other un-closed run names as `Parent` — `magic:think-deep`'s rule;
  never author a second definition. **Several un-closed leaves** (parallel runs) ⇒ `status` / bare
  `resume` **ASK which**, never guess.
- **Destructive-op safety.** `clear` never deletes an un-closed live leaf without an explicit confirm.

## list [all]
Outline the **unfinished** runs only (no Gate-log verdict line; `Closed: no`). Glob `think-*.md` in the scratchpad; per un-closed run:
- **id** (filename stem) · task (`# Execution Protocol:` line)
- **steps** — ticked / total from `## Steps`
- **lineage** — its `Parent` chain
- mark the **live leaf**.

Terminal runs (a Gate-log verdict line, or the legacy header-only `Closed: done|escalated`) are omitted unless `all` is given.

## status
Show the **current think tree** — the live leaf and its `Parent` lineage, root → leaf, each node with its
step `k/total` and `Closed` state, the live leaf marked. No un-closed run ⇒ report **no live tree** (point
at `list all`).

## clear [all]
Delete protocol files, safety-scoped:
- **default** — remove only **terminal** runs (a Gate-log verdict line, or the legacy header-only `Closed: done|escalated`); print a manifest of what was removed.
- **`clear all`** — remove every `think-*.md`, behind an explicit confirm.
- **never** delete an un-closed **live leaf** without an explicit confirm.

## resume [<id>]
Re-enter a run — `resume <id>` (named) or bare `resume` (the live leaf). Re-establish the `[think] <id>`
marker, then hand off to `Skill(magic:think-deep)`, which re-opens `think-<id>.md` via its **existing**
carried-id fast path / disk-fallback. Zero-touch — select the run and set the marker; never fork the
reconstruct logic.

## export [<id>] [<dir>]
**Copy** (never move) `think-<id>.md` to a durable dir (default `docs/working/<feature>/`). Keep the
filename; version-suffix on a clash; leave the scratchpad original for the live run. Run export before a planned `/clear`: a clear rotates the scratchpad.

## continue <path>
Re-enter think-deep on an **externally exported** protocol file by **explicit path** (no auto-discovery).
The manager first flattens a `Parent:` pointing at a gone scratchpad to a root (one-line notice; ASK if >1
candidate root), then hands off to `Skill(magic:think-deep)`, which mints a fresh scratchpad id on entry.

## When NOT to use
- To **execute** a think task → `magic:think-deep` (bare `think!! <task>`), never this.
- To change think-deep's phases or its carried-id / disk-fallback model → out of scope; read it, never redefine it.
