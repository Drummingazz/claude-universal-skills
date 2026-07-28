---
name: gigscan
description: Daily gig-email sweep for The Gareth Cohen Experience. Scans Gareth's connected Gmail for messages from the four booking agencies (Rhythm Culture, Soul Drummer, African Drumming, Drumbeats) that read as a gig opportunity, proposal, offer, or confirmation, and alerts him to each. On a confirmation specifically, it extracts the gig details and creates the Google Calendar event automatically under the Calendar Naming Protocol 2026, colour-coded yellow for workshops and purple for performances, after checking the calendar so a manually entered event is never duplicated. Use when Gareth says "gig scan", "/gigscan", "scan agency emails", "check for gig confirmations", or as the daily automated sweep.
---

# Gigscan

Output one header line before anything else: `[Gigscan] — DD MMM YYYY HH:MM AEST` using the current date and time in AEST.

Reads and alerts are free. Calendar event creation on a confirmed gig is the one auto-write this skill performs without a separate approval step, matching the existing rule in [[Engines/GCE/booking-pipeline]] and the [[Engines/GCE/agent-roster|Command Secretary]]: once a booking is accepted, the calendar event is created automatically because the acceptance itself was the approval, and Gareth is notified. Everything else (replying to the agency, rescheduling, cancelling, a gig with a missing required field, anything sensitive) stops and waits for Gareth.

## Scope

Watch for messages from or clearly referencing these four agencies (source codes per [[Engines/GCE/calendar-naming-protocol]] and [[Engines/GCE/agencies-and-channels]]):

| Agency | Source code |
|---|---|
| Rhythm Culture | RC |
| Soul Drummer | SD |
| African Drumming | AD |
| Drumbeats (also written "drum beats") | DB |

Sender domains are not confirmed in the vault yet, so search by name, not just `from:`. Do not assume a sender is one of these four agencies from domain alone if the name isn't confirmed; use the message content to confirm.

## Step 1: Search Gmail

Search the connected Gmail account (Gareth's "GC Gmail", read via the Gmail connector) with a query covering the last 2 days (a 2-day window gives overlap in case a run is missed, and duplicate alerts are prevented in Step 3):

```
("Rhythm Culture" OR "Soul Drummer" OR "African Drumming" OR "Drumbeats" OR "drum beats") (gig OR booking OR workshop OR performance OR opportunity OR proposal OR offer OR confirm OR confirmed OR confirmation OR available OR availability) newer_than:2d
```

If this returns nothing, also run a plain agency-name-only search (no keyword filter) over the same window in case a relevant email uses none of those words, and read the top results to judge relevance manually.

## Step 2: Classify each thread

For each matching thread, read the full message (not just the snippet) and classify as one of:

- **Opportunity / proposal / offer**: the agency is proposing, asking about availability, or floating a gig that is not yet locked in.
- **Confirmation**: the gig is locked in. Look for explicit confirmation language ("confirmed", "booked", "locked in", "go ahead", "yes please proceed") or a reply accepting a date/fee Gareth or the agency already put forward.
- **Not relevant**: agency admin, invoicing, or non-gig correspondence. Skip.

Check the state log described in Step 6 before alerting, so a thread already surfaced in a previous run is not re-alerted, only its status change (opportunity to confirmation) is reported.

## Step 3: Alert

Every opportunity, proposal, offer, and confirmation gets surfaced to Gareth, grouped by agency, in this shape: agency, one-line summary, date and location if known, status (opportunity or confirmed), and for a confirmation whether the calendar event was created or what's missing. Plain English, no dashes, mobile-friendly, matching [[Identity/me]] output preferences.

If nothing relevant was found, say so in one line. Do not pad the report.

## Step 4: On a confirmation, extract the gig details

Pull from the thread (and prior messages in the same thread if needed for context):

- Source code (RC, SD, AD, or DB)
- Role code: default FAC (Facilitator) unless the thread specifies support or co-facilitation, per [[Engines/GCE/calendar-naming-protocol]]
- Type of service: the service category, e.g. School Workshop, OSHC Workshop, Corporate Team Building, NDIS Group Workshop, Performance (updated 2026-07-15: this must be the category, never a restatement of the agency or activity the Source Code already implies, "African Drumming Incursion" is not a valid value for an AD-sourced gig, that's redundant with the source code)
- Drum count
- Max participants
- Sessions and duration
- Age group or year level
- Company, org, school, or client name (never left blank)
- Full address
- Date, session start and end time, and arrival time if stated (arrival time may differ from session start)
- Any fee mentioned
- Any timezone stated

**Drum count and max participants are never assumed.** If either is missing, or the date, time, or address is missing, do not create the calendar event. Instead flag the gig as an incomplete confirmation in the alert and say exactly what's missing, so Gareth or the Bookings Manager can chase it. This mirrors the field rule already in the Calendar Naming Protocol.

## Step 5: Classify workshop vs performance for colour

- **Workshop** (colour: yellow, colorId `5` / Banana): team building, NDIS or school sessions, lessons, classes, corporate sessions, anything facilitation-style.
- **Performance** (colour: purple, colorId `3` / Grape): shows, concerts, festivals, stage performances, anything where Gareth is performing rather than facilitating.

If the type is genuinely ambiguous, default to yellow (workshop is GCE's core service) and note the assumption in the event description and in the alert to Gareth.

## Step 6: Check for an existing calendar entry before creating one

Before creating anything, call `list_events` (or a full-text search) on Gareth's primary calendar for a window covering the gig date (±1 day). Treat it as an existing manual entry, and skip creation, if an event on that date matches on any two of: the org/client name, the full address, or the source agency code. Report "already on the calendar, no duplicate created" in the alert rather than creating a second event.

Maintain a small state log at `Engines/GCE/gigscan-processed-log.md` in the vault: one line per thread ID already alerted or already turned into a calendar event, with the date. Check it at the start of Step 2 and append to it after Step 3 and Step 7 each run, so re-runs don't re-alert or re-create.

## Step 7: Build and create the event

Follow [[Engines/GCE/calendar-naming-protocol]] exactly:

Title (updated 2026-07-15, full address dropped, title ends at the org/school/client name):
```
[Source Code] [Role Code] | [Type of Service] | [Drum count] drums | [Max participants] max | [Sessions and duration] | [Age group or Year] | [Company, org, school, or client name]
```

- Full address is not in the title. It goes in the Location field (set it explicitly via the calendar tool's location parameter so it's clickable through to maps, not just typed into the description), and can also appear further down in the description if useful.
- Description format (updated 2026-07-15): starts with "Contact:" followed by the site contact's name and phone number as a clickable `tel:` link. Then type of service (fuller narrative detail is fine here, unlike the title category), session schedule, drum count, and any purpose, notes, or access information. Do not include the booking agency's own name or email addresses, and do not include a line noting arrival time is unstated, just state it if known and omit the line if not. Never put NDIS disability or support detail in the title, description only. The confirmed fee goes last, at the very bottom of the description, the final settled figure only, not the negotiation (no offer, counter-offer, or back and forth).
- Blocking window: the event spans exactly the stated session time, arrival or start through to finish, with no buffer either side, unless the gig specifies a different arrival or setup requirement (updated 2026-07-15, see [[Engines/GCE/calendar-naming-protocol]] for the superseded 60-minutes-each-side default). Put the session start and end time in the description.
- Reminders (updated 2026-07-15, see [[Engines/GCE/calendar-naming-protocol]]): one email 24 hours before arrival (or session start if no arrival stated). No other email. If arrival/start is at or after 10:00am, also add a single popup 3 hours before; if arrival/start is before 10:00am (early morning), no same-day reminder at all.
- Timezone rule: if there is any timezone discrepancy, flag it in BOLD CAPS in both the title and the description.
- colorId `5` for a workshop, `3` for a performance, per Step 5.

Create the event, then tell Gareth in the alert that it's on the calendar and editable.

## Step 8: Session log

Write a short entry to `Daily/YYYY-MM-DD.md` (today's date) noting what was scanned, what was found, what was created, and what's still missing or waiting on Gareth. Skip this step only if the scan found nothing at all.

## Guardrails

- Never invent a price, date, address, contact, or commitment. Mark anything unclear as MISSING and escalate rather than guess.
- Never restart a qualification sequence on an already-qualified lead.
- Never contact the agency or reply on Gareth's behalf. This skill reads, alerts, and writes calendar events only. Drafting or sending a reply is out of scope, hand that to [[Engines/GCE/agent-roster|the Bookings Manager]] or the Command Secretary.
- Sensitive content (NDIS, school, vulnerable-client wording) still gets created on the calendar per the NDIS privacy rule above, but flag it for [[gce-risk-reviewer]] review in the alert rather than treating it as routine.

## Related

- [[Engines/GCE/calendar-naming-protocol]]
- [[Engines/GCE/agencies-and-channels]]
- [[Engines/GCE/booking-pipeline]]
- [[Engines/GCE/agent-roster]]
