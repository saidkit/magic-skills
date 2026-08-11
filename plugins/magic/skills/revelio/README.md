# revelio — a quick "where were we?" recap of a long chat

**What it is.** When a conversation has gotten long and you've lost the thread, `revelio` sweeps back through it and hands you a short, fresh recap: what's been happening, where the work stands right now, any rules or limits you set earlier that still matter, and a shortlist of what to do next. Then it stops and waits for you.

**When to reach for it.**
- "We've been at this a while — where were we, and what's left?"
- You stepped away and came back cold, and need the picture again.
- Before you decide the next move, you want the constraints you mentioned earlier pulled back up so you don't forget them.
- A lot has scrolled by and the important bits are buried above.

**How to call it.** Just type `revelio` (or `revelio!`). Nothing else needed.

**What you get back.** A tidy refresh in a few short sections: recent activity, the current state of the work, the constraints you set in earlier turns, and 3-5 next actions listed in priority order. It skips whatever's already right there in the last couple of messages — repeating that would just be noise. It does *not* start doing any of the work; it hands you the picture and pauses.

## Examples

**You type:** `revelio`
**You get back:** A recap like — "Recent: you refactored the checkout page and fixed two failing tests. State: the payment step works; the confirmation email is still stubbed out. Constraints you set: keep everything in TypeScript, no new dependencies. Next: (1) wire up the real email send, (2) add a test for the empty-cart case, (3) update the changelog."

**You type:** `revelio!`
**You get back:** The same kind of refresh after a break — "Where we left off on the auth work: login is done, password reset is half-built. You asked to keep the API shape unchanged. Next up: finish the reset token flow, then the rate-limit check."

**You type:** `revelio`  (early in a short chat)
**You get back:** A brief note that there isn't much to refresh yet — the whole conversation is still right above you.

## Good to know
- It only refreshes and stops — it won't continue the work on its own. Tell it what to do next, or use the `locomotor!` macro to refresh *and then* keep going.
- Each call is a one-time, fresh sweep. Nothing it tells you is remembered into later turns, so call it again whenever you need another look.
- Related helpers: `pensieve` gives a fuller, whole-project status audit laid out as a table; `muggle` explains one specific thing in plain English.
