# Operator macros — the paste-in half

The `magic` plugin ships the four skills. This file ships the **macros that drive them**.

A Claude Code plugin cannot add text to your `CLAUDE.md`, and the macros are the ergonomic layer: they let you type `revelio!` mid-sentence instead of `/magic:revelio`, and they define the autonomy verbs (`expelliarmus`, `locomotor!`) that the skills refer to when they say "do not continue unless paired with `locomotor`".

Without this block the skills still work — you invoke them as `/magic:revelio`, `/magic:pensieve`, `/magic:lumos`, `/magic:session`. With it, they work the way they were designed to.

## Install

Paste the block below into **`~/.claude/CLAUDE.md`** (applies to every project) or a project's **`./CLAUDE.md`** (that project only).

## The block

```markdown
# Operator macros

## `expelliarmus` / `expelliarmus!`

Standing OK to proceed through all phases / batched tasks / multi-step flows without further confirmation pauses, until natural completion or a hard blocker. Skip phase-to-phase waits, batch boundaries, and rule-by-rule `next` waits for the remainder of the invocation. Still REPORT each phase boundary; only the wait goes — **never a stage or a gate**. A suppressed confirmation pause never removes the step it guarded (a verification / acceptance / debrief stage still runs; autonomy drops the wait, not the work). Does NOT carry across invocations.

Hard blocker = unsatisfiable approach, failing quality gate needing a decision, ambiguous scope creep, or a destructive operation outside scope.

## `revelio` / `revelio!`

Execute the `/magic:revelio` skill.

## `locomotor!`

Run `revelio!`, then proceed through its next-actions list autonomously to full completion, as if the operator typed `expelliarmus!` — same hard-blocker rules, same no-carry-across-invocations, same no-new-stages constraint. The operator may interrupt between phases by sending a new message; otherwise both phases run in one response.

## `pensieve!`

Execute the `/magic:pensieve` skill.

## `pensieve locomotor!`

Run `pensieve!`, then proceed through the remaining path autonomously as if `expelliarmus!` were active, stopping only at natural completion or a hard blocker.

## `lumos` / `lumos!`

Execute the `/magic:lumos` skill.

## `session!`

Execute the `/magic:session` skill.

## `think!`

Execute the `/magic:think-deep` skill.

## `auror!`

Invoke `/magic:think-deep` for the user-specified task: build a plan, execute autonomously, cross-verify the results, and deliver a final report.

**Enforcement:** the FIRST action on `auror!` is to call the `/magic:think-deep` skill. Not satisfied by "proceeding autonomously" — doing the work without invoking the skill is emulation. Haven't invoked it this turn? Stop, invoke it.

If the task body names a macro or pipeline, pass it to think-deep **intact** — do not pre-summarize it into generic steps. The plan must **bind that pipeline to its actual skills** (invoke them; never emulate inline), and surface the skills it will invoke.

Proceed as if `expelliarmus` is active: report phase boundaries, but do not wait at them. Stop only at natural completion or a hard blocker. Does NOT carry across invocations.
```

## Notes

- **`expelliarmus` is load-bearing.** `locomotor!` and `pensieve locomotor!` are defined in terms of it, and `/magic:pensieve` names it in its stop condition. Keep it even if you never type it directly.
- **Keep the `!` suffix meaningful.** Across this macro family the bare word and the `!` form do the same thing; the `!` is a readability cue that the operator means the macro, not the English word.
- **Macros do not carry across invocations.** This is deliberate — every macro is scoped to the message that invoked it, so an autonomy grant can never silently persist into later work.
