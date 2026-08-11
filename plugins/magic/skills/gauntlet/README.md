# gauntlet — hand you a ready-to-paste prompt that builds something until it matches a reference you name

**What it is.** `gauntlet` writes a strong, copy-paste "build-to-a-bar" prompt for you. The prompt tells an AI to split the work into parts, put a builder and a harsh critic on each part, and keep going until every part matches or beats an example you point at — judged blind, side by side.

**When to reach for it.**
- "Build me this, and don't stop until it's as good as that example."
- "I want it broken into parts, each one pushed to top quality, not just 'good enough.'"
- "Give me a reusable prompt I can paste into another tool and run there."
- "I have a reference to aim at, and I want the bar held that high."

**How to call it.** Type `gauntlet! <what you want>` (or `/magic:gauntlet <what you want>`). Always name something to compare against — a reference image, an example, or a well-known thing. No reference, and it will stop and ask you for one.

**What you get back.** A ready-to-paste prompt (in one block) that you copy and run wherever you like. Important: gauntlet only writes the prompt — it does not run the build itself. You paste it and press go.

## Examples

**You type:** `gauntlet! a landing page as polished as ref/hero.png`
**You get back:** A copy-paste prompt that splits the page into parts (hero, pricing, footer…), loops on each with a harsh critic checking it against `ref/hero.png`, and won't stop until each part wins a blind side-by-side.

**You type:** `gauntlet! a product card as clean as ref/card.png`
**You get back:** The same kind of prompt, aimed at your card example — ready to paste into another tool and run there.

**You type:** `gauntlet! a polished dashboard` (no reference)
**You get back:** A pause and a question — "what should I compare it against?" — because there's nothing to hold the bar to yet.

## Good to know
- It prints, you run. gauntlet hands you the prompt; running it happens wherever you paste it.
- It needs something to compare against. Point at a reference (like `ref/hero.png`) or it will ask for one first.
- Close cousin of `critic!` — `critic!` sets the finish line and can do the review itself; `gauntlet` just hands you a strong prompt for a build-to-a-bar loop you run elsewhere.
