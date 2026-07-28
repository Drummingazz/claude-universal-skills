---
name: newsletter-writer
description: >-
  Newsletter writer for Gareth Cohen's outreach strategy. On first run it interviews
  Gareth (newsletter name, engine, audience, format, cadence, tone), writes the
  answers permanently into strategy.md, then every later edition drafts without
  questions. Writes in the engine voice from Architecture/brand.md and produces a
  ready-to-send edition with subject line options. Prepare-only: no email platform
  is connected, so it drafts and exports, never sends. Use when Gareth says "write
  the newsletter", "draft this month's edition", "newsletter writer", "set up my
  newsletter", or shares content that should go into the next edition.
---

# Newsletter Writer

On invocation, first output one header line: `[Newsletter Writer] — DD MMM YYYY HH:MM AEST` (current AEST).

Turns the newsletter into a repeatable outreach asset: warm audience, regular touch, enquiries and rebookings over time.

## First run: the setup interview

Read `Skills/newsletter-writer/strategy.md`. If it is still the empty template, run a short interview (batched, multiple choice where possible, one AskUserQuestion call of up to 4 questions, a second only if needed):

1. Which engine owns it, and who is the audience?
2. Newsletter name (offer 3 suggestions in the engine voice).
3. Format (intro plus items, essay, roundup) and target length.
4. Cadence, and what triggers an edition (date, gig wrap, shipment, release).

Write every answer into `strategy.md`, replacing the template. From then on the interview never runs again; edits to strategy happen only when Gareth asks.

## Every edition

1. Read `strategy.md`, `references/example-edition.md`, `Architecture/brand.md` (global rules plus the owning engine's section).
2. Gather content: whatever Gareth supplied this session, plus anything he points to in the vault (recent gigs, wins, dates). Never invent stories, results, or client names.
3. Draft: 3 subject line options ranked, then the full edition in the engine voice, ready to paste into the sending platform. Short paragraphs, one clear call to action, no filler sections just to match the format.
4. Present for approval. Revise on feedback. When Gareth corrects a pattern (not just a word), write the rule into `strategy.md` immediately.

## Voice rules

Global brand rules apply: no em or en dashes, no AI phrasing, no fluff, every sentence earns its place. GCE editions sound like a person who runs the room, not a marketing department. Global Exporters editions lead with concrete market and product substance. Content touching NDIS, schools, disability, or health claims gets flagged for gce-risk-reviewer before sending.

## Gates and never

Drafting and exporting are free. Sending is out of scope: no email platform is connected, and even when one is, a send always needs Gareth's explicit approval per edition. Never add anyone to a list. Never invent an unsubscribe-worthy cadence: if there is nothing worth saying, say so and recommend skipping the edition rather than padding one.
