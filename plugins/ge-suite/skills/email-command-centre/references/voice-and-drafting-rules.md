# Voice and Drafting Rules

How a Global Exporters email should read, the non-negotiable formatting rules, the
freight-specific logic, and how to log to the vault afterwards.

## Gareth's voice

Professional, warm, and direct. He is a real person running a real early-stage export
business, not a corporate form letter. Write the way a switched-on founder writes to a
freight forwarder or a setup firm he respects and wants a fast, useful answer from.

- Get to the point early. Say what you want and why in the first few lines.
- Courteous, not stiff or fawning. A brief thank-you for their time is fine; gushing is not.
- Confident and specific. Reference the actual route, commodity, container, or question
  rather than vague generalities. Specifics earn faster, better replies.
- Plain English. No jargon padding, no filler, no "I hope this email finds you well."
- Honest about where things stand. He is comfortable saying the business is at an early,
  exploratory stage and is comparing options. He does not over-promise volumes or commit
  to anything not yet decided.

## Formatting rules (hard)

- **No long dashes. None.** No em dashes and no en dashes anywhere in the email. Use a
  comma, a full stop, a colon, or restructure. This is the single most important
  formatting rule, because the output goes to outside parties and it is Gareth's standing
  rule across everything.
- **Sign off at "Kind regards," then Gareth's signature.** Drafts are created through
  Composio's API, which does not auto-insert the Outlook signature, so the skill supplies it:
  after "Kind regards," append Gareth's signature block (name, company and phone in bold, the
  email in red) and the inline logo, exactly as set out in
  `references/composio-draft-recipe.md`. Do not invent a different signature.
- **Use a numbered list when asking for more than one thing.** It lets the recipient reply
  point by point, which is exactly how freight and setup queries get answered cleanly.
  For a single ask, prose is fine.
- **Highlight what matters, in context.** Bold the few details most important to the
  recipient given the email's purpose: money and rates for quotes, the metrics for size,
  volume, mass or timing asks, the binding terms for agreements, and so on. Choose what to
  bold using `references/highlighting-rules.md`. Bold sparingly; if everything is bold,
  nothing is.
- Keep paragraphs short. A greeting line, the substance, the ask, then "Kind regards,".
- Match the subject line to the thread. For a reply, keep or lightly tidy the existing
  subject (e.g. prefix "RE:"). For a new email, write a clear, specific subject.

## Freight drafting logic

Global Exporters exports fresh produce from Adelaide / Two Wells, South Australia to
Dubai, UAE, under wartime Gulf conditions. The whole point of a freight thread is to get
a quote to the state where it can be priced and trusted. So every freight reply should
push toward resolving the **five fields** that make a quote pricing-ready:

1. War risk surcharge.
2. Destination charges.
3. Inland trucking (the road leg from the discharge port to Dubai).
4. Genset / temperature control continuity on the inland leg (the biggest cold-chain
   risk; the most commonly omitted item).
5. Marine and road insurance.

Apply these rules when drafting:

- **"Via Fujairah" or "via Khor Fakkan" is not a clean direct Jebel Ali route.** In the
  current wartime Gulf context, treat a routing stated as "Jebel Ali via Fujairah" or "via
  Khor Fakkan" as most likely meaning the cargo discharges at Fujairah or Khor Fakkan and
  moves on to Dubai / Jebel Ali by road or bonded land bridge. Do not overstate it as
  impossible that the vessel continues to Jebel Ali by sea, but the default commercial and
  cold-chain risk assumption is that a via-port means a road on-carriage leg until the
  carrier confirms otherwise in writing. So ask them to confirm the actual routing rather
  than assuming a clean sea discharge at Jebel Ali.
- **Frame cold-chain questions as a confirmation request, never as an instruction on how to
  do their job.** These are freight professionals. Do not write "Is the truck
  genset-equipped?" as if telling them their business. Ask them to confirm the arrangement
  and who carries the risk. Canonical phrasing to adapt:

  > Given the quote states Jebel Ali via Fujairah, can you please confirm whether the
  > Fujairah to Dubai / Jebel Ali leg is by road or bonded land bridge, and if so, whether
  > that leg is covered under continuous reefer temperature control, including genset power,
  > temperature monitoring, and liability for any temperature excursion?

  A shorter acceptable form when routing is not the focus:

  > Can you please confirm whether any on-carriage or road leg is handled under continuous
  > temperature-controlled reefer conditions, including whether genset power and temperature
  > monitoring are included?

  The point is to confirm what is already in place and who is liable, not to dictate
  equipment.
- **Provide commodity and cargo value when a quote or insurance figure needs it**, so the
  carrier can quote properly. Default test parameters, unless Gareth specifies otherwise:
  - Commodities (durable sea-freight produce): potatoes, onions, garlic, carrots,
    pumpkin, sweet potato, cabbage. Optional premium comparison: Valencia oranges, table
    grapes.
  - Origin: Adelaide / Two Wells, South Australia. Destination: Dubai, UAE.
  - Equipment: 20ft and 40ft reefer. Assumed max load up to 27,000 kg (road-limited).
  - Sea cargo insurance value tests: AUD 50,000 and AUD 100,000 per container.
  - Air premium test shipment (when air is the thread): 2,000 to 3,000 kg, insured value
    AUD 30,000 to 50,000.
- **Do not send buyer-facing pricing.** Freight numbers can be discussed with carriers;
  landed-cost or sell pricing to buyers is gated until margin validation is complete.

If a reply would require a freight figure or a farm gate price that is not in the vault,
do not invent it. Ask Gareth, or leave a clearly marked placeholder for him to fill.

## Logging to the vault after a draft is created

Follow the vault's conventions (see the vault `CLAUDE.md`): use `[[wikilinks]]` for every
entity (people, carriers, engines, notes), never use long dashes, keep notes inside an
existing folder (never the vault root), and prefer updating an existing note over creating
a competing one.

After a draft is created or handed over:

- Add a dated one-line entry to the thread's owning note. For freight that is
  `Freight-Intelligence-Log.md` (e.g. "2026-06-02: Drafted clarification reply to
  [[Nathan Borg]] at [[Seaway Logistics]] requesting routing, genset, war risk,
  destination charges, insurance, transit time.").
- If the reply creates a follow-up or changes who owes what, update `Next-Actions.md`.
- File reference detail to the right note automatically (carrier/provider detail to
  `Carrier-Contact-Register.md`; setup-firm detail to
  `UAE-Professional-Services-Outreach.md`; credentials auto-saved to
  `Account-Credentials-and-Portals.md`, recording service, login URL, username,
  credential and date; confirm only service and username in chat, never the credential).
- If the email maps to an Airtable record, note in the summary that the record should be
  updated. Do not write to Airtable from this skill.
- Report exactly which notes were created or updated, which were skipped, and which (if
  any) already held the information.

## Worked tone example (freight clarification)

This is a model for tone and structure, not a script to copy. Note: no long dashes, a
numbered list for multiple asks, ends at "Kind regards,".

```
Hi Nathan,

Thank you for the reefer quotation. Before we can compare it properly against the
other carriers and model the landed cost, I need to close a few gaps. Could you confirm
the following in writing:

1. The routing. The quote shows Jebel Ali via Fujairah. In current Gulf conditions we are
   assuming the Fujairah to Dubai leg is by road or bonded land bridge unless you confirm
   otherwise, so could you confirm whether the cargo discharges at Fujairah and moves on by
   road, or whether the vessel continues to Jebel Ali by sea? If there is a road leg, is it
   bonded?
2. If there is an on-carriage or road leg, could you confirm it is covered under continuous
   reefer temperature control, including genset power, temperature monitoring, and who
   carries liability for any temperature excursion?
3. The war risk surcharge, stated separately.
4. Destination charges at Jebel Ali.
5. Marine and road insurance options, for cargo values of AUD 50,000 and AUD 100,000
   per container.
6. The total transit time, port to door.

Once I have these I can put your quote on an equal footing with the others. Thanks again.

Kind regards,
```
