---
name: think-outside-the-box
description: Fast macro-goal sanity check — pauses before (or during) a nontrivial multi-step plan, restates the actual objective in one line, and weighs a couple of genuinely different ways to get there, including the boring/obvious one. Catches tunnel vision before it burns hours making a specific tool, integration, or sub-approach work when the real goal never needed it. Use when Gareth says "/think-outside-the-box", "zoom out", "bigger picture check", "are we overcomplicating this", "step back", or "is there a simpler way". Also self-invoke this proactively and silently, unasked, whenever about to commit to a plan with several steps or multiple tools/integrations, a task is dragging on longer than it should, or troubleshooting a tool has replaced pursuing the actual goal — run it as a quick internal check before continuing, not something that interrupts Gareth. A gut-check, not a formal review — no reports, no scoring.
---

# Think Outside The Box

## Why this exists

Gareth once burned an enormous amount of time trying to get two faulty MCPs to talk to each other so a dashboard could sync live across multiple accounts. The actual goal was just "a dashboard that stays live and current for whoever looks at it." That's what hosting it at a single URL gives you automatically — no sync needed, no integration to fight. The specific technical path (getting the MCPs to cooperate) quietly became the goal itself, and nobody stepped back to ask whether it was even necessary. This skill is that "stepping back" moment, made cheap enough to actually use.

## When to run it

Explicit triggers: "/think-outside-the-box", "zoom out", "bigger picture check", "are we overcomplicating this", "step back", "is there a simpler way", "talk me out of this path."

Self-invoke it quietly, without asking permission or interrupting, when any of these show up:
- about to commit to a plan with several steps, or one that wires together multiple tools/services/MCPs
- a task is taking noticeably longer than it felt like it should
- the last few steps have been about getting a tool, API, or integration to cooperate rather than about the original ask
- you're about to write a workaround for something that's broken instead of asking whether that thing was needed at all

This is meant to run in a breath, as part of your own reasoning before you act — not as a pause that hands control back to Gareth or asks him extra questions. Only surface it to him if the check actually turns up something worth flagging.

## The check

Do this in a few sentences, not a document:

1. **Name the macro goal, one line.** Not the sub-task you're currently stuck on — the thing that actually needs to be true when this is done, from the perspective of whoever asked for it. If you can't state it in one plain sentence, that's itself a sign you've drifted.

2. **Generate 2-4 genuinely different routes to that goal.** Not variations on the current approach — actually different mechanisms. Always include the boring/obvious option (the one that skips clever integration entirely), even if it feels too simple or "not what was asked for." The current in-progress approach is one of the options being compared, not the default winner.

3. **Ask honestly: is the current approach still the best of these, or is it winning by inertia** because time's already sunk into it? Sunk cost is not a reason to continue. A path that's fighting a broken or uncooperative tool is a strong signal something simpler exists.

## Verdict

Close with one short line, not an essay:

- **"Proceed as planned — [one clause why it's still the best option]."**
- **"Simpler/better alternative worth considering: [the alternative] — [one clause why]."**

If the verdict is to switch course, say so plainly and briefly to Gareth before continuing, so he can veto it — don't silently redirect a task he's expecting to see finished a certain way.

## Example

Task in progress: "make it so this dashboard shows the same live data whether Gareth or his assistant opens it, by getting MCP-A to push updates to MCP-B every few minutes."

- Macro goal: both people see the same current data whenever they look.
- Alternatives: (a) MCP-to-MCP sync job [current path], (b) host the dashboard at one URL both people open — it's live by construction, nothing to sync, (c) one shared data source both dashboards read from directly, (d) scheduled export both people pull from.
- Check: the current path only exists because two separate copies were assumed necessary. They weren't.
- Verdict: "Simpler alternative worth considering: host it at one live URL instead of syncing two copies — same result, nothing to keep in sync, no MCP plumbing to maintain."
</content>
</invoke>
