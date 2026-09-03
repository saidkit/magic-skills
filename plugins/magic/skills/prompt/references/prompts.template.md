# Prompt library
<!--
Your house prompt library — read + curated by `prompt!!`. One shot per `##` block:

    ## <case label> — <when to use, one line>
    <the prompt, terse, exactly as you'd type it>

The `## case — when` header is how `prompt!! <ask>` matches; the body is what it mimics.
`prompt!! add` appends new shots here (least-verbose); you can also hand-edit this file.
Keep it terse and human-readable — it's the bridge between you and the model.
-->

## code-review — reviewing a diff before merge
Strict correctness review of the current diff: flag bugs, edge cases, and anything that breaks an existing contract. Skip style. Rank by severity, cite file:line. Don't fix — report.

## commit-message — writing a commit for a finished change
Terse conventional-commit for the staged change: a `type(scope): summary` subject under 72 chars, then 2–3 body lines on what and why (not how). No filler.
