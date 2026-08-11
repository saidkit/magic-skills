# critic — turn a fuzzy quality goal into a clear finish line, then check your work against it

**What it is.** `critic` takes a vague standard like "make it good" or "as good as that page" and pins it down into a concrete, finishable "done-when" bar — then reviews your target against that bar. No more review loops that run forever.

**When to reach for it.**
- "I want this to look as good as that example, but I can't say exactly why."
- "Get this to production quality — no serious bugs left."
- "Is this actually done, or am I just tired of looking at it?"
- "Give me a checklist I can hand to a teammate so we agree on 'good.'"

**How to call it.** Type `critic! <target>` (also `criticize! <target>` or `/magic:critic <target>`). The target can be a file, a folder, or just a plain description of what you want judged. It only fires when you say one of those words — a plain "review this" won't trigger it. Then add a mode word after the target:
- **(nothing)** = review — the default. It reports what it finds and changes nothing.
- **`+fix`** = repair — it reviews AND fixes until clean. This is the only mode that touches your files.
- **`as prompt`** = export — it hands you the "done-when" as a short prompt you can save or share.

**What you get back.** A pinned "done-when" contract (the exact bar you're aiming for) plus a ranked list of findings — each one says where it is and why it matters, worst first. Because the bar is concrete, it also tells you clearly when to stop.

## Examples

**You type:** `critic! review the pricing page against ref/hero.png`
**You get back:** A blind side-by-side bar based on your example image, a ranked list of what's off (spacing, color, alignment), and zero edits to your files.

**You type:** `critic! get the checkout flow to production quality +fix`
**You get back:** A "done-when" of "zero serious issues and tests green," then the actual fixes applied until it clears that bar.

**You type:** `critic! turn "make the dashboard world-class" into a done-when as prompt`
**You get back:** A short, reusable prompt with a clear finish line — ready to paste into a new task or hand to a teammate.

## Where it really shines

The three examples above are the everyday cases. Here's what critic can *really* do — each is a pattern pulled from live sessions:

**1. Make a runaway "make it perfect" loop actually stop.**
`critic! make our pricing hero as polished as ref/hero.png` → instead of a vibe or a 1–10 score, it writes a *checkable finish line*: judge each part (headline · CTA · visual · layout) **blind** against your image, pass at ≥4 of 5 looks, brand colors in-kit. *"Perfect" has no ceiling and invites the builder to rubber-stamp itself; "beats this reference, judged blind" converges — and blind judging blunts the self-flattery.*

**2. Adversarially review something already generated — and catch contradictions a search can't.**
`critic! review this generated spec corpus` → a hard pass that finds *semantic, cross-file* defects a quick reread skims past: a stale rule stated as if current, two files that quietly disagree, a section that teaches the very mistake it warns against. Findings come back ranked in a review file — and by default it **changes nothing.**

**3. Point it at a security or correctness job — it refuses the fake beauty contest.**
`critic! harden our password-reset flow` → it *knows* there's nothing to eyeball, so it doesn't fake a look-and-feel comparison. It pins a threat checklist and writes a repair bar instead — *attacker-stance review until zero serious findings, security tests green* — automatically taking the attacker's view on anything touching money, data, or security.

**4. Fuse "looks right" and "is correct" into one anchored run.**
`auror locomotor! build the revenue dashboard — matches ref/dash.png and every number reconciles` → critic authors a **combined** bar (recompute every figure against the source = zero discrepancies **and** the charts blind-vs-example ≥4/5, both required), then a build → judge → fix-the-weakest → re-judge loop runs it until it clears the bar **or escalates — it never quietly declares victory.**

**5. Reuse the bar, or repair with it.**
`critic! <target> as prompt` exports the pinned "done-when" as portable text you can paste anywhere or hand a teammate; `critic! <target> +fix` is the explicit opt-in that actually repairs the target. One hard-won "how do I know it's good?" you can reuse across many jobs.

## Good to know
- **No example to compare against?** For a look-and-feel goal with nothing to point at (`critic! make it stunning`), it stops and asks you for a reference rather than inventing one — even on autopilot. An unpinned bar is how you end up with beautifully-polished *wrong* work.
- The default is review, which is safe and never edits your files. Add `+fix` only when you actually want it to make changes.
- It needs an explicit word to start — `critic!`, `criticize!`, or `/magic:critic` — that's on purpose, so it never fires by accident.
- Pairs well with `auror!` when you want the whole review-and-fix loop run for you, start to finish.
