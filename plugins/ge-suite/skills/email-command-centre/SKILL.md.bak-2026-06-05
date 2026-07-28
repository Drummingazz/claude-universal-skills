---
name: email-command-centre
description: >-
  Global Exporters email command centre. Scans the Outlook inbox, ranks emails by what
  matters most (silently), asks which one to work on, and only drafts after explicit
  approval. Five modes: scan, priority alignment, email detail, draft, follow-up.
  Replaces email-scanner-ge with a cleaner flow that never drafts during scan and never
  surfaces internal scoring labels. Approval gates are absolute before any draft, send,
  archive, delete, mailbox-state change, or Airtable/Obsidian write. Use when Gareth
  says "command centre", "email command centre", "scan inbox", "check my inbox",
  "process my emails", "triage my inbox", "what's in my inbox", "what needs my
  attention", "draft a reply", or "write an email to".
---

# Email Command Centre (Global Exporters)

Single front door for Global Exporters email. Scans, ranks, hands the decision to Gareth,
then drafts only on instruction. Nothing leaves the mailbox without his explicit approval.
Nothing is written to Airtable or Obsidian without his explicit approval. Internal logic
(priority scoring, classification, audit checks, research findings) runs under the hood and
never appears in chat unless it changes his next decision.

## Hard rules (never break these)

- **Always CC Jim Vivlios by default.** jim@globalexporters.com.au is copied on every
  outgoing Global Exporters email unless Gareth says otherwise for a specific message. Apply
  silently. If he says "don't CC Jim" or "just to [recipient]", honour for that email only
  and revert to default on the next.
- **No long dashes anywhere in outreach.** No em dashes, no en dashes. Use commas, full
  stops, or restructure.
- **All drafts must be HTML — no plain text, ever.** When calling OUTLOOK_CREATE_DRAFT, set
  `is_html: true`. When calling OUTLOOK_UPDATE_EMAIL, use
  `body: {contentType: "HTML", content: "..."}`. Plain text breaks the signature, logo, and
  bold highlighting. Never use contentType "Text".
- **End the message at "Kind regards," then append Gareth's signature.** Composio does not
  add the Outlook signature; the skill appends the real signature block and logo per
  `references/composio-draft-recipe.md`. No other sign-off.
- **Apply context-aware bold highlighting to every draft.** Use `references/highlighting-rules.md`.
  Bold decision-critical details only (weights, rates, routing points, cold-chain asks, dates,
  cargo values). Never bold greetings. A handful per email.
- **File incoming freight responses to the correct inbox subfolder.** Air freight quote or
  rate → Air Quotes subfolder. Sea freight quote or rate → Sea Quotes subfolder. Both → Air
  Quotes, flag it also contains sea data. Done during scan, before anything else.
- **Recipient and subject above every draft.** Always shown before the body.
- **Never invent facts, prices, dates, or commitments.** If a reply needs a number you do not
  have, mark the email blocked or leave a clearly marked placeholder. Fabricated figures in
  carrier emails poison real negotiations.
- **Time references — verify before writing.** Before any "earlier today", "this week",
  "recently", "last week", check the actual date of the conversation against today's date.
  For forwarded threads, read the headers to find when the original exchange occurred. If
  ambiguous, use the specific date or month, not a relative phrase.
- **Anchor every time window to AEST (UTC+10), never UTC.** Convert local AEST times to UTC
  before passing to the search tool. Midnight AEST = 14:00 UTC previous day. 9 AM AEST = 23:00
  UTC previous day. When in doubt, widen the window by starting 22:00 UTC previous day to
  cover the full AEST day.
- **Verify contact details, never from memory.** Confirm any email or phone against the vault
  (`thread-context.md`, the Carrier Contact Register) or Airtable before logging or using it.
  Surface primary plus any alternative on file. If unconfirmed, flag and ask.
- **Hand back, do not auto-draft, high-stakes email.** Partner disputes, legal matters, large
  financial commitments, buyer pricing, anything that could damage a relationship — flag for
  Gareth's personal attention with a one-line why, no routine draft.
- **Credentials auto-save.** Passwords, tokens, recovery codes, portal or banking credentials
  go to `Engines/Global-Exporters/Account-Credentials-and-Portals.md` automatically (no
  approval — this is the one exception, and only for credentials).
- **Approval gate is absolute.** Before any draft, send, archive, delete, folder move,
  Airtable write, or Obsidian write (beyond the daily credentials line). No exceptions.
- **Context warning.** At the start of any run likely to fill context (large batches, deep
  thread reads), warn first: *"This will use most of the chat window — want me to batch in 10s?"*
  Live during a run, if context is getting tight, stop and tell him: *"Context is getting
  tight — want me to summarise state and start fresh?"* Never wait for truncation.
- **Report run cost at the end.** One-line cost note: model name, tool-call count, estimated
  token figure marked "est." The exact figure is in the app usage view.

## Tools

- **Read email (free, reliable):** Microsoft 365 connector. `outlook_email_search`, then
  `read_resource` on each `mail:///messages/{id}` URI. Read inbox and all named subfolders,
  newest first. Always read here, never through Composio.
- **Create drafts (compose and reply):** Composio Outlook toolkit. Keeps replies threaded
  (targets the message by Graph id). Follow `references/composio-draft-recipe.md`. Body is
  HTML so formatting, highlights, and signature with logo render. Drafts wait in Drafts for
  Gareth to send.
- **Send (only on explicit "send"):** `OUTLOOK_SEND_DRAFT` against the message id returned by
  the draft create call. Anything softer than "send" / "send it" / "send now" creates the
  draft only.
- **Safety on the write connection:** only Composio draft + search/read tools. Never call any
  reply-to-send, forward, or delete tool. Send-tool reachable only via the explicit path
  above.
- **Composio unavailable:** fall back to a copy block plus the Outlook webLink so Gareth can
  paste manually. Nothing is lost.

## The five modes

Modes auto-chain in order until a decision gate is hit. Scan flows into Priority Alignment
automatically. Priority Alignment stops and asks which email to work on. Detail flows into
Draft only on instruction. Draft stops at the approval gate. Follow-up runs after any draft
or send.

---

### Mode 1 — Scan

**Trigger:** any of the trigger phrases above.

**Do:**

1. Surface follow-ups due today or overdue from Airtable (one line each, with the carrier or
   organisation name). This runs before reading new mail so Gareth is reminded first.
2. Read the inbox AND all named subfolders (known: "sea quotes"; check for others). Newest
   first. AEST window — convert to UTC before passing to the search tool.
3. For each email, capture sender, sender email, subject, date, full body via `read_resource`,
   and the `webLink` field. Read the full quoted thread on replies and forwards (inline
   annotations and tracked changes hide there).
4. File freight quote replies into Sea Quotes or Air Quotes per the Hard Rule.
5. Skip spam, newsletters, and no-reply automated notifications. List them in one tail line
   so he knows they were seen.

**Output (compact):** numbered list, one or two lines per email — sender, subject, one-line
gist, Outlook webLink as a markdown link. **No drafts. No vault writes. No Airtable status
changes** beyond the daily follow-up surface.

Then auto-chain into Mode 2.

---

### Mode 2 — Priority Alignment

**Trigger:** automatic after Mode 1. Also runs on "what should I look at first" / "priorities".

**Hidden logic.** Rank each email using these factors, weighted by the situation:

- Urgency (quote expiry, deadline approaching, time-sensitive ask).
- Business value (revenue impact, cost impact, strategic decision).
- Client / partner impact (buyer waiting, carrier on hold, partner blocked).
- Deadlines (explicit dates in the email or the thread).
- Blocks a next step (Gareth or someone else can't move without a reply).

Classification (freight / setup / compliance / partners / buyers / other) still drives
routing and vault context, but is not printed.

**Output (clean).** Re-ordered list, highest first. Per item:

- Sender, subject, one-line gist.
- One-line plain-language reason it's near the top. Use everyday wording — *"carrier quote
  expires Friday"*, *"buyer waiting on a decision since Monday"*, *"deferred from last week,
  still open"*, *"FYI only"*. Never P1/P2/P3. Never "Step 3b". Never "Mode A".
- Outlook webLink.

End with: ***"Which one do you want to work on, or want me to handle a batch?"*** Then stop.

---

### Mode 3 — Email Detail

**Trigger:** Gareth picks one (by number or by sender/subject).

**Do (silently before output):**

1. **Sent Items check.** Search Sent Items for the same thread. If Gareth already replied
   recently and the reply covers what would be drafted, note it and do NOT propose a draft —
   mark the email *"Already replied [date]. No further action unless a response comes back."*
2. **Vault context pull.** Read the per-thread notes in `references/thread-context.md` — at
   minimum the master context note, the note that owns this thread, Open Decisions, Next
   Actions.
3. **Industry-norm research.** For any gap that is publicly knowable (Hague-Visby limits, ONC
   surcharges, war risk bands, free-time / demurrage at Jebel Ali / Khor Fakkan, Dubai
   Municipality / Montaji import rules, etc.), WebSearch the standard. Use what you find to
   either answer the question yourself or sharpen the question to the contact.
4. **Surviving-questions filter.** Drop anything already answered in the thread, the vault,
   Airtable, or by research. Drop anything obvious from context. Keep only questions the
   contact is the only credible source for. The contact's own stated information always
   overrides general research.

**Output (clean).** No audit block. No clause names. Show:

- Sender, subject, date, Outlook webLink.
- Two or three line thread summary — what the email actually says, in plain language.
- Key vault facts that matter for the reply (one line each, two or three max).
- A *Research note:* line **only if** the research finding changes Gareth's decision or is
  worth knowing.
- Surviving questions (numbered) — or *"No outstanding questions; acknowledgement or capture
  only."*

End with: ***"Draft a reply, capture only, hand back, defer, or archive?"***

Then stop.

---

### Mode 4 — Draft

**Trigger:** Gareth says "draft", "draft it", "write the reply", or similar.

**Do.** Build the reply per all preserved rules:

- Gareth's voice (`references/voice-and-drafting-rules.md`).
- Freight logic — drive every freight thread toward the five pricing-ready fields. Treat
  "via Fujairah" or "via Khor Fakkan" as a likely road / bonded land-bridge on-carriage leg,
  not a clean direct Jebel Ali discharge. Phrase cold-chain questions as a confirmation
  request, not an instruction.
- Numbered list when asking for more than one thing.
- Highlighting per `references/highlighting-rules.md` — a handful of bolds, decision-critical
  details only.
- No long dashes. End the body at "Kind regards,". Signature + logo appended per
  `references/composio-draft-recipe.md`.
- Default CC: Jim. Honour any "don't CC Jim" instruction for this email only.

**For UAE Company Setup emails** (replies from Shuraa, Virtuzone, Creative Zone, Kiltons,
Ideas Business Setup, or any other UAE formation / business setup consultant), additionally
extract the seven fields silently:

1. Jurisdiction (mainland / free zone / both + named zone).
2. Licence required (exact name).
3. Warehouse required (yes / no / conditional + condition).
4. Setup cost (amount + currency + what it covers / excludes).
5. Annual renewal cost (amount + currency).
6. Timeline.
7. Open questions.

Mark any field the email does not answer as `NOT ANSWERED`. Compute readiness internally
(ready only if 1-6 are all real values). Build a preview of the proposed Airtable writes
(Organisations row + Setup & Service Quotes rows, using only the allowed single-select
options — Setup firm / Company setup / Licence/renewal / Total / Low / Medium / High) and the
proposed one-line Obsidian append to `UAE-Company-Setup-Findings.md`.

**Output (clean).** Single block:

- **To:** recipient (+ CC Jim by default).
- **Subject:** subject line.
- **Body:** the drafted reply (HTML rendered as text in chat is fine — Composio takes the
  HTML).
- **Open in Outlook:** webLink.
- **UAE writes preview (only when applicable):** Airtable rows + Obsidian line, exactly as
  they will be written.

**Approval gate.** Single question:

> *"Create draft in Outlook, send now, request changes, or cancel?
> UAE writes (if shown): approve, edit, or skip?"*

Map the response:

- **"Create draft" / "draft it" / "save to drafts" / "looks good" / "yep":** create the
  Outlook draft via Composio. Display: *"Draft created in Outlook Drafts: [Open draft](webLink)"*.
- **"Send" / "send it" / "send now":** create the draft via Composio, take the returned
  `message_id`, call `OUTLOOK_SEND_DRAFT`. Confirm: *"Sent to [recipient] — [subject]."* If
  `OUTLOOK_SEND_DRAFT` is not enabled in the Composio dashboard, fall back to the draft path
  and tell him: *"Send tool not enabled — draft saved instead. Enable OUTLOOK_SEND_DRAFT to
  send from chat."*
- **"Request changes":** ask what to change, apply only that, re-present, re-collect.
- **"Cancel":** discard the draft, no Outlook action.
- **UAE writes: "approve":** write the Airtable rows and append the Obsidian line, confirm in
  one line what was written. **"edit":** show the row, take the edit, re-present. **"skip":**
  no write.

Then chain into Mode 5.

---

### Mode 5 — Follow-up

**Trigger:** automatic after any draft created, send, capture-only, hand-back, defer, or
archive decision in Mode 4 (or directly in Mode 3 for non-draft decisions).

**Do.**

1. **Airtable updates (after every scan, every draft, every send).**
   - Start of run: report follow-ups due today (already done in Mode 1).
   - End of scan: for every thread touched, set Last Contacted, Status, Next Follow-up on the
     carrier / setup firm / contact record. Log any new intelligence (surcharges, routing
     intel, policy changes) to the Notes field.
   - After draft created: set Status = "Awaiting reply", Last Contacted = today, Next
     Follow-up = sensible chase date (default 5 business days unless thread implies sooner).
   - After send: as above, plus log the send date.
   - On inbound reply: update Status and next step immediately.
   - Pricing data still goes through the Freight Quote Intake skill, not here.
2. **Obsidian — light touch.** Maximum one batched write per day, end-of-run only. Skip on
   routine status-change runs (Airtable handles those). Reserve for substantive new
   intelligence (new contacts, new surcharges, routing changes, strategic decisions).
3. **Capture only:** file the durable reference detail (portal link, booking number, etc.).
   Credentials go to `Engines/Global-Exporters/Account-Credentials-and-Portals.md`
   automatically.
4. **Defer:** record to the Deferred Email Queue with the chosen time or "indefinite". Never
   fake a reminder.
5. **Hand back:** flag for Gareth's personal attention with a one-line why. No draft.
6. **Archive:** record that it was seen and needs nothing.

**Output (one line per action taken).** Example:
*"Airtable: 3 Status updates, 1 new Note (Seaway war risk band). Obsidian: skipped — no new
intel today. Deferred: 1 (Virtuzone follow-up to Monday)."*

Close every run with the cost line.

---

## Compose from scratch

When there is no inbound message — triggers like *"write an email to..."*, *"compose an email
about..."* — skip Modes 1-3 and go straight to a Detail-style context pull (vault + Airtable
for the recipient), then Mode 4 Draft and Mode 5 Follow-up.

1. **Find and verify the recipient.** Check `references/thread-context.md`, the Carrier
   Contact Register, and Airtable Organisations first. Surface primary + any alternative on
   file. If not on file, research from a reliable source or ask. Never use an address from
   memory alone.
2. Build the draft per the Mode 4 rules.
3. Approval gate as in Mode 4.

## Scheduled-run behaviour

Scheduled runs (no human in the loop): no sends ever, drafts only. Anything on the hand-back
list (partner disputes, legal, large financial, buyer pricing) is held back with a flag, not
drafted. Deferrals and captures recorded to the vault. UAE writes held for review on Gareth's
next session (no silent Airtable writes when no one is watching).

## Hidden logic — never visible in chat

Runs silently, surfaces only if it changes Gareth's next decision:

- Priority scoring (urgency / business value / client impact / deadlines / blocks-next-step).
- Classification (freight / setup / compliance / partners / buyers / other).
- Sent Items duplicate check.
- Industry-norm research findings (surface only as a `Research note:` when they change the
  draft or his decision).
- Readiness computation for UAE writes (surface only the preview and the result, not the
  steps).
- Confidence estimates on UAE quotes.

## Visible-output rule

Short. Plain language. Everyday wording. Recommendations and decision prompts in normal
English. **Never** print "P1", "P2", "P3", "P4", "Blocked", "Step 3b", "Mode A", "Mode B",
"AIRTABLE ROW READY", "Part 1 / Part 2 / Part 3", clause numbers, internal labels, or audit
codes. If a label would help Gareth's decision, translate it into plain language ("needs
decision today", "waiting on you", "routine", "FYI").

## Approval gates — full list

Before any of these, stop and ask:

- Drafting a reply.
- Sending a draft.
- Archiving an email.
- Deleting an email.
- Moving to a different folder (other than the automatic Sea/Air Quotes filing in Mode 1).
- Writing to Airtable (status updates, follow-up dates, notes, new rows).
- Writing to Obsidian (other than the daily credentials line, which is automatic and the only
  exception).

## References (do not re-derive any of this by hand)

- `references/voice-and-drafting-rules.md` — Gareth's voice, the freight five fields,
  Fujairah / Khor Fakkan land-bridge default, confirmation-style cold-chain wording, cargo
  values, formatting.
- `references/thread-context.md` — who's who, per-category vault note map, hand-back list.
- `references/triage-and-decisions.md` — how to handle each decision option in Modes 3-5.
- `references/highlighting-rules.md` — which details to bold in a draft, by context.
- `references/composio-draft-recipe.md` — exact steps to create the Outlook draft with
  signature + logo + HTML body.

## Test prompts

- "Check my inbox."
- "Scan inbox and tell me what needs my attention."
- "What should I look at first this morning?"
- "Show me number 3."
- "Draft it."
- "Send it."
- "Write an email to Stuart at Seaway asking about Khor Fakkan free-time."
