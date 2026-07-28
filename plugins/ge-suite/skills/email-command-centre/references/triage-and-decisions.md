# Triage and Decisions

The full handling for the decision options, the internal priority scale, and the Deferred
Email Queue. SKILL.md gives the short version; come here for the detail when Gareth picks
an option. The approval gate and the no-long-dashes / "Kind regards," rules apply throughout.

## Note for Email Command Centre

This reference was originally written for the linear `email-scanner-ge` workflow. In the
Email Command Centre, the decision options are surfaced **in plain language only** -- never
as a numbered menu, never with internal labels. Use this file as a reference for *how* to
execute each option, not for *what to print* in the chat.

- The decision word **"Escalate"** has been renamed to **"Hand back"** in the Command Centre.
  Treat any mention of "escalate" below as "hand back" -- same meaning, same handling.
- The decision prompts have moved:
  - In **Mode 3 (Email Detail)** Gareth picks: *"Draft a reply, capture only, hand back,
    defer, or archive?"*
  - In **Mode 4 (Draft)** Gareth picks: *"Create draft in Outlook, send now, request changes,
    or cancel?"* (plus, for UAE Company Setup emails, *"UAE writes: approve, edit, or skip?"*)
- The priority scale below (P1-P4 + Blocked) runs **silently** in the Command Centre and is
  translated to plain-language reasons in Mode 2 output ("needs decision today", "waiting on
  you", "routine", "FYI"). Never print "P1" / "P2" / "P3" / "P4" / "Blocked" to chat.

## Priority scale

Assign one priority per email at classification time. Handle highest first.

| Priority | Meaning |
|---|---|
| **P1 Critical** | Time-sensitive, project-blocking, quote expiry, legal or compliance, a buyer response that needs a decision. |
| **P2 Important** | Freight quote clarification, partner coordination, business setup, active supplier or provider follow-up. |
| **P3 Normal** | Routine admin or low-pressure correspondence. |
| **P4 Low** | FYI, newsletters, low-value updates. |
| **Blocked** | A reply is needed but cannot be drafted properly because required information is missing. Always name the missing item and the proposed next action. |

## The six handling options

These are the six ways an email can be handled. Do **not** print them as a numbered menu in
the chat. There are no live buttons there, and Gareth will simply tell you, often by
dictating, what he wants. Suggest the handling you think fits in one natural line, then map
whatever he says, in his own words, to one of these:

**Approve, Request changes, Defer, Escalate, Capture only, No action / archive.**

### 1. Approve

Proceed according to the available connector and approval rules.

- If an Outlook 365 draft/reply tool is connected, create the reply (or new email) as a
  **draft**, addressed correctly and threaded to the original. Confirm it is waiting in
  Drafts. **Never auto-send.**
- If Outlook draft creation is **not** available (read-only connector), say so clearly and
  hand back the finished, copy-ready text for Gareth to paste. Do not pretend a draft was
  created.
- Then log per SKILL.md Step 7 and file any reference detail.

### 2. Request changes

Do **not** blindly rewrite. Ask what amendments Gareth wants first, offering quick options
so he can answer in a word or two:

- shorter
- warmer
- firmer
- more professional
- more casual
- add detail
- remove detail
- ask fewer questions
- ask more directly
- soften wording
- rewrite a specific paragraph
- preserve structure but change tone

Apply only what he asks for, keep every hard rule (no long dashes, ends at "Kind regards,",
recipient and subject shown, no invented facts), then re-present the revised draft and
re-collect the decision. Repeat until he approves, defers, or drops it.

### 3. Defer

Park the message until a chosen time or indefinitely. Treat "skip" as a defer with no
follow-up required.

Defer options:

- later today
- tomorrow morning
- in 2 days
- next Monday
- before quote expiry
- custom date/time
- indefinitely / no follow-up required

**Honesty rule:** if no real reminder, task, or calendar tool is connected at run time, do
not claim a reminder was scheduled. Instead record the item (or propose recording it) into
the **Deferred Email Queue** in Obsidian, or as a Next Action, or into Airtable Tasks if
that is the agreed home. If a reminder/task/calendar tool *is* connected and Gareth wants
it used, you may set the reminder, but still also record the queue entry so nothing is lost.

Deferred Email Queue lives at `Engines/Global-Exporters/Deferred-Email-Queue.md` (create it
inside the Global-Exporters folder if needed, never the vault root). Record these fields per
deferred item:

- **Sender**
- **Subject**
- **Priority** (P1-P4 or Blocked)
- **Reason deferred**
- **Defer until** (date/time or "indefinitely")
- **Required missing information** (what unblocks it, if Blocked)
- **Proposed next action**
- **Owner** (usually Gareth; sometimes Jimmy, Dimi, or Kumar)
- **Draft status** (no draft / draft saved in Outlook / paste text held)

### 4. Escalate

For email that is sensitive, legal, financial, high-value, strategic, conflict-risk,
unclear, or that needs Gareth's personal judgement. Hand it to him with a one or two line
note on why, instead of drafting a routine reply. Cross-reference the escalation list in
`thread-context.md`. Typical escalations: partner disputes or money disagreements (Dimi,
Jimmy), anything legal, large or binding financial commitments, and buyer requests for
pricing or quotes (gated until margin validation is complete). Flagging is not ignoring:
record it in the run summary and, if it will be picked up later, add it to the Deferred
Email Queue so it is not lost.

### 5. Capture only

Extract the useful information from the email into Obsidian or Airtable, but do not draft a
reply. Use this for portal links, usernames, freight contact details, quote references,
booking references, account setup details, and compliance instructions. File all detail
(including credentials) automatically per "Capturing reference detail" in SKILL.md. No
per-item approval is required for credentials.

### 6. No action / archive

For low-value email or anything that needs no response. Equivalent to "defer indefinitely /
no follow-up required". Note that it was seen and needs nothing, so it is not silently
dropped. No draft, no capture unless something useful is worth keeping.

## Credential auto-save rule (applies to every option)

Passwords and credentials found in email are **automatically written to the vault** at
`Engines/Global-Exporters/Account-Credentials-and-Portals.md` (create if needed, never the
vault root). Record: service name, login URL, username, credential, and date captured. Do
not scatter credentials elsewhere. Do not ask for per-item approval. Report to Gareth what
was saved by confirming the service name and username only; do not reproduce the credential
itself in the chat summary.
