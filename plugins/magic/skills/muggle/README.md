# muggle — explain what's going on, in plain English

**What it is.** A quick way to get a jargon-free explanation of where things stand or what something means. Think of it as "explain it like I'm not steeped in the details."

**When to reach for it.**
- You want a plain-English gut-check on what's happening right now.
- Someone handed you a technical change and you just want to know what it actually does.
- You need a sentence you could forward to a teammate who isn't technical.
- You're a bit lost and want the short version, without the history or the internals.

**How to call it.** Type `muggle!` — on its own, or with what you're curious about, like `muggle! what does the caching change do?`

**What you get back.** A short, warm explanation in everyday language: the gist, where things stand, and the practical "so what." No code, no jargon, no formal status report — just a clear answer you could read out loud.

## Examples

**You type:** `muggle! explain what this change actually does`
**You get back:** A couple of plain sentences: what the change is for, what's different now, and why it matters — without walking through the code.

**You type:** `muggle! what's going on right now?`
**You get back:** A quick, human summary of the current state and what it means for you — no status tables, no acronyms.

**You type:** `muggle! give me something I can send to a non-technical teammate`
**You get back:** One clear, shareable sentence or two that anyone can follow, safe to paste into a message.

## Good to know
- muggle is the most casual of three siblings. `revelio!` refreshes your working context and suggests next actions; `pensieve!` gives a full, structured status table. Reach for muggle when you just want it explained simply.
- It deliberately skips implementation detail and long history — if you need the full picture, use `pensieve!` instead.
- Perfect for a fast sanity check or for sharing with someone outside the weeds.
