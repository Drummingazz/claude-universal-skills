---
name: ge-debug-verify
description: "HARD-GATED debugging verification protocol for the Global Exporters Command Centre app"
---

---
name: ge-debug-verify
description: >-
  HARD-GATED verification protocol for the Global Exporters Command Centre app
  (command-centre-app/public/ge-command-centre.html). Invoke this BEFORE saying any bug is
  fixed, any feature is done, or any change works in that app. It forbids the words
  "fixed / done / working / verified" until the validation gate passes, the bug's own check
  flips RED then GREEN in the live preview, window.geSelfTest() returns ok:true, the console
  is clean, and evidence is written to TESTING-LOG.md. Anything that needs a live model,
  Outlook, Airtable, or a real send is labelled "needs your live retest", never "done". Use
  when Gareth says "verify", "is this fixed", "before you say done", "test this", "run the
  gate", "/ge-verify", or whenever an edit to command-centre-app is about to be reported as
  complete.
---

# GE Command Centre — Verification (HARD GATE)

This skill exists because "fixed" was claimed before things were tested and they broke on the
first real click. It turns "I checked it" into "the named check was RED, it is now GREEN, the
suite passes, and here is the logged evidence."

- App under test: `command-centre-app/public/ge-command-centre.html` (single-file Node/Express
  + inline-JS dashboard).
- Working directory for commands: `command-centre-app/`.
- Gate command: `node checkge2.js public/ge-command-centre.html` (must print `blocks=3 errors=0`).
- In-app harness: `window.geSeedFixtures()` (seed a hard board + reload) and `window.geSelfTest()`
  (run the invariant suite, returns `{ok, problems}`).

---

## THE HARD GATE (non-negotiable)

You MUST NOT write the words **fixed, done, working, verified, complete, or implemented** for any
change to this app unless EVERY item below is GREEN in the current session:

1. **Gate green:** `node checkge2.js public/ge-command-centre.html` prints `blocks=3 errors=0`.
2. **Red→Green proof:** the bug was first expressed as a concrete check that you ran and saw FAIL
   (red); the same check, after the fix and a preview reload, now PASSES (green).
3. **Invariant suite green:** `window.geSelfTest()` returns `ok:true`.
4. **Console clean:** `preview_console_logs` at level `error` returns no errors after the interactions.
5. **Evidence logged:** a row was appended to `TESTING-LOG.md` recording the red→green check and the
   suite result.

If ANY item fails, it is NOT done; say what failed and keep working.

If an item CANNOT be run in this sandbox (no live Anthropic model, no Outlook/Composio, no Airtable,
no real send), label that part **"needs your live retest"** and never "done". Front-end behaviour is
always testable here; backend / AI / live behaviour is not.

Screenshots are NOT acceptable proof on this page (~13 MP4 loops stall capture). Prove visual state
with `getComputedStyle` / class names / DOM assertions, which are more accurate anyway.

---

## QUICK RUN (the happy path, with the harness)

1. `preview_start` name `command-centre`; in `preview_eval` run `window.geSeedFixtures()` (seeds + reloads).
2. Express the bug as a check and run it → confirm it is **RED**.
3. Find the root cause (read the code path), make the smallest fix that keeps the send-gate intact.
4. Gate: `node checkge2.js public/ge-command-centre.html` → `blocks=3 errors=0`.
5. Reload the preview; re-run the bug's check → **GREEN**; run `window.geSelfTest()` → `ok:true`.
6. Adversarial: break the invariant once, confirm `geSelfTest()` flags it, undo.
7. `preview_console_logs` (error) → none. Append the evidence row to `TESTING-LOG.md`.
8. Report with the honesty ledger (proven here vs needs your machine).

---

## STEP-BY-STEP (full)

1. **Express the bug as a falsifiable check.** Turn "chip 13 has no box" into an assertion you can
   run (e.g. count visible cards vs chips by number). No vague "looks wrong".
2. **Reproduce it (capture RED).** Start the preview, run `geSeedFixtures()`, run the check, record
   that it FAILS. If you cannot reproduce it, do NOT proceed to "fixed"; say so and ask for the exact
   state.
3. **Find the root cause, not the symptom.** Read the actual code path end to end and name the cause
   (e.g. "two independent dedup passes that can disagree"). State cause vs patch.
4. **Make the smallest fix** that addresses the cause. Keep safety logic intact: the
   `lightColor` / `cardIssues` / `batchState` send-gate must never be weakened so an unfinished draft
   can send.
5. **Gate:** `node checkge2.js public/ge-command-centre.html` → `blocks=3 errors=0`.
6. **Reload and confirm the new code loaded** (grep a marker string from your edit in the page's
   `script` text). Do not test a stale page.
7. **Re-run the bug's check → GREEN.** Drive the REAL flow: click the real button, fire the real
   event. Confirming a function "exists" is NOT a test.
8. **Run the invariant suite:** `window.geSelfTest()` → `ok:true`.
9. **Adversarial check:** if you added a guard, deliberately break the invariant once and confirm the
   guard fires, then undo.
10. **Console clean** at error level.
11. **Write evidence** to `TESTING-LOG.md` (format below).
12. **Report** with the honesty ledger.

---

## FIXTURES

Run `window.geSeedFixtures()` in `preview_eval`. It builds one hard board (every department, every
status, a duplicate thread, a saved card, an empty-subject card) and reloads, then verify against it.
Edge cases are where the bugs live, so never verify against a single easy card.

To exercise the statuses after seeding, drive the REAL controls: click a card's `.ftappr` (approve →
green light 2), its reply-bar Save-to-drafts button (→ green + pink DRFT OUTLK), and its `.statlight2`
(→ sleep / grey, box + chip dim).

If `geSeedFixtures` is ever missing, the raw seed is the `seed` object inside `function geSeedFixtures`
in `ge-command-centre.html`; paste it into `localStorage.setItem('ge_autocards', JSON.stringify(seed))`,
clear `ge_(status|saved|filed|done)_*` keys, and reload.

---

## INVARIANT SUITE

Call `window.geSelfTest()` in `preview_eval`; require `ok:true`. It lives in the app (search
`function geSelfTest` in `ge-command-centre.html`) and asserts the CONTRACTS:

- every visible card has a chip with the same number, and vice versa (no orphans, no duplicates);
- light 2 on every card matches `geStatusLight` (light 1 stays the department colour);
- the diagonal bar AND Batch Send both equal `geAggStatus` (aggregate draft status).

These are written as user-facing truths, not function names, so they survive internal refactors.

**Keeping it from rotting (the maintenance rule):**
- When you change a behaviour a check covers, update the check IN THE SAME edit. The checks live in
  `ge-command-centre.html` next to the code they test, so that is natural.
- Add a NEW assertion to `geSelfTest` whenever a NEW contract is introduced (e.g. a third light).
- A check that fails because it is STALE (the app changed, the check didn't) is a bug to fix, not a
  result to trust. Prefer loud false alarms over silent misses.

Fallback (only if `geSelfTest` is absent): the equivalent inline assertion is the body of
`function geSelfTest`; copy it into an IIFE in `preview_eval`.

---

## HONESTY LEDGER (always state this)

Cannot be tested in this sandbox; always tag "needs your live retest":
- Live AI replies (no Anthropic model key here).
- Outlook send / draft create / archive (Composio not connected).
- Airtable reads/writes and Obsidian notes.
- Real two-monitor HP projection and any real `window.open` popup behaviour.

CAN be tested here: rendering, colours/classes (computed styles), DOM structure, click/keyboard
flows, localStorage state, the validation gate, console errors.

---

## TESTING-LOG ENTRY FORMAT

Append a row to `command-centre-app/TESTING-LOG.md`:

`| <short title> | front-end ✅ verified end-to-end / 🟡 needs retest | <the RED check, the fix, the
GREEN result, geSelfTest ok:true, what was driven by real clicks, what still needs Gareth's machine,
gate blocks=3 errors=0> |`

Never write "✅ verified" on anything you did not actually run.

---

## FAILURE HANDLING

- **Gate red (`errors>0`):** a syntax break. Fix before anything else; nothing downstream is valid.
- **Cannot reproduce:** do NOT claim a fix. Report that you could not reproduce and ask for the exact
  state (Gareth's localStorage / board) or steps.
- **Suite red after the fix:** the fix caused a regression; treat the regression as the new bug and
  restart the loop. Never ship a fix that breaks an invariant.
- **Stale-page suspicion:** hard-reload and re-confirm the new code is loaded before trusting any result.