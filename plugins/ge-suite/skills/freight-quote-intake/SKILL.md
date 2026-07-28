---
name: freight-quote-intake
description: >-
  Capture an incoming freight quote into the Global Exporters OS Airtable base.
  Use whenever Gareth shares a freight, shipping, or reefer quote from a carrier or
  forwarder (Seaway, MSC, CMA CGM, DHL, CT Freight, Kuehne + Nagel, Team Global
  Express, and others) for sea reefer, sea dry, or air freight out of Australia
  (usually Adelaide) to the UAE. Triggers include
  "log this quote", "add this freight quote",
  "here's the reefer rate from…", "enter this into Freight Quotes", forwarding a
  rate email, or pasting ocean/air freight pricing. The skill
  extracts every field, marks anything absent as MISSING, converts to AUD at a live
  rate (storing the exact rate and timestamp), scores completeness, rates cold-chain
  risk and competitive position, links the Route and Freight Provider records, then
  PREVIEWS the mapped record and waits for explicit approval before writing anything
  to Production. Use it even if Gareth never says "skill" or "Airtable" — any time a
  freight quote needs capturing, this is the tool.
---

# Freight Quote Intake

Global Exporters exports Australian fresh produce to the UAE under **wartime Gulf
conditions**. Freight quotes arrive fast, expire fast, and are frequently
incomplete in exactly the places that decide whether a shipment is safe and
profitable — war risk surcharge, destination charges, inland trucking, genset
(reefer temperature control on the road), and insurance. A quote that *looks*
complete but is silent on genset can destroy a 22-tonne reefer of produce on an
18-hour inland haul.

Your job is to turn a raw quote into a clean, structured, honestly-flagged record
**so the team never acts on an incomplete quote without knowing it's incomplete** —
and to put a human approval step between parsing and any write to the live base.

## Two rules that override everything

1. **Never invent, infer, estimate, or "reasonably assume" a value that is not in
   the quote.** If a field is not stated, it is `MISSING` — not a guess, not a
   typical market figure, not a number copied from another carrier. Resolved states
   are fine and honest: `EXCLUDED` (carrier says it's not included), `INCLUSIVE`
   (carrier says it's included), `Not Confirmed` (expected but not stated),
   `Not Applicable`. The only thing you may compute is the AUD conversion (Step 2),
   and you must record the exact rate and timestamp.
   Note on contacts: the record's Contact Name / Contact Email fields get **only**
   what the quote itself states. The known contacts in `routes-and-providers.md` are
   for addressing your follow-up action, not for backfilling the record — if the
   quote omits the contact email, it is `MISSING`.

2. **Never write to the Production base without explicit approval.** Default
   behaviour is a dry-run preview. You parse, map, score, and show — then you stop
   and ask. You only call `create_records_for_table` (and only create Route/Provider
   records) after Gareth says yes. This is non-negotiable: a wrong record in the
   live base poisons every downstream pricing decision.

## Workflow

Read `references/airtable-schema.md` once at the start (exact base/table/field IDs,
select options, write recipe, Notes-block template), `references/routes-and-providers.md`
(canonical routes + known carrier contacts), and `references/scoring.md` (the
completeness, cold-chain, and competitive rubrics). Don't re-derive any of it by hand.

### Step 1 — Ingest and extract

The quote may be pasted email text, a forwarded message, or an attached file
(PDF / DOCX / image / spreadsheet). If a file is attached, read it; if it's an image
or scanned PDF, read it visually. Extract every field below, each **exactly as
quoted** (keep original currency and units) or marked `MISSING`:

Carrier / forwarder · contact name · contact email · quote date · **validity / expiry
date** · freight method (sea reefer / sea dry / air) · container type or air weight
tier · port of loading (usually Adelaide) · port of discharge (Jebel Ali / Khor
Fakkan / Sohar / Salalah / Fujairah) · routing / transhipment detail · ocean/air base
rate + currency · origin charges (itemise in Notes) · destination charges · war risk
surcharge · bunker / emergency fuel (BAF / EBS) · inland trucking cost · marine
insurance · road insurance · customs / duties · demurrage / detention terms + free
time · empty-container return responsibility · **genset / temperature control on the
inland leg — confirmed or not** · reefer plug availability at discharge · transit
time · commodity restrictions · Incoterms · exclusions / conditions · any other notes.

**Capture every clause, subclause, footnote, and disclosure, wherever it sits in the
message.** Read the whole email and every attachment top to bottom, including anything
printed **below or after** the rate table, in email footers and signature blocks, in
small print, or on trailing pages, because carriers routinely put binding conditions
there. That covers validity and rate revision clauses, subject to confirmation and
subject to space wording, surcharge and currency adjustment clauses (BAF, CAF, GRI,
PSS, war risk, low sulphur), liability limits, force majeure, detention and demurrage
subclauses, routing caveats, and legal disclaimers. Bring each one through **verbatim**
into the Notes block under the `Clauses & fine print` line; never paraphrase a condition
into something softer, and never drop one because it looked like boilerplate. If a
clause can move a number or a risk (for example a war risk or BAF clause that lets the
rate change), also reflect it in the relevant field or flag, and apply Rule 1: record it
as stated and never invent the figure it might become.

### Step 2 — Convert to AUD and store the FX provenance

Quotes mix currencies (ocean usually USD, Australian origin charges AUD, UAE-side
sometimes AED). Convert non-AUD base freight to AUD so quotes are comparable, and
**store the conversion permanently so historical quotes stay comparable even after
rates move**:

- Look up the live mid-market rate by web search ("USD to AUD today").
- `FX Rate Used` (`fldsbGspltPyWFwTy`, precise) = the exact rate, e.g. `1.3917`.
- `FX Rate Captured At` (`fldLp32Tbj5CZIo9A`) = e.g. `2026-06-01 USD to AUD mid-market`.
- `Freight Cost` (`fldrgWVwhSbl6tPpV`) keeps the **original** amount; `Currency`
  (`fldIFpl9Wd1C7wBFN`) keeps the **original** currency.
- `Freight Cost (AUD)` (`fldWgarGiVRqgA0au`) = the converted AUD amount.
- Leave the legacy `AUD Conversion Rate` (`fldqTIcgVUhiljPUY`) blank — it rounds to
  an integer; `FX Rate Used` supersedes it.
- State the rate in the summary as a dated assumption. If you genuinely cannot get a
  rate, leave the AUD fields blank, say why, and flag it. Never fabricate a rate.

### Step 3 — Score completeness, cold-chain risk, competitive position

Per `references/scoring.md`:
- `Quote Completeness %` (`fldESahiKp62hbOl3`) — weighted 0–100, critical fields
  count double. Show the breakdown (`critical X/9, standard Y/11`).
- `Cold Chain Risk` (`fld9DOtJ7UBW0xfUC`) — **sea reefer only**; Low / Medium / High
  / Unknown. Default to **High** when a sea-reefer quote is silent on genset. Leave
  blank for air / sea-dry.
- `Competitive Position` (`fldHLobBluphYRffI`) — compare against existing quotes on
  the same route+method. **Default Cannot determine** when any critical charge is
  missing or there's no comparator.

### Step 4 — Resolve (don't yet create) the Route and Provider

Map the discharge port to a canonical route and the carrier to a provider (tables +
payloads in `references/routes-and-providers.md`). Search the Routes and Freight
Providers tables to see whether each already exists. **Do not create them yet** — you
create and link them only at the write step, after approval. If the discharge port
matches no canonical route (e.g. air to DXB), don't force it: leave Route unlinked
and flag it.

**Routing-ambiguity rule (wartime — Rule 1 applied to routing).** A phrase like "to
Jebel Ali **via Fujairah**" does **not** confirm a clean direct discharge. "via [port]"
is unresolved: the cargo might discharge at the via-port and move on by bonded road /
**land bridge**, the vessel might call there then continue by sea, or it might tranship
onto another vessel. The three cases carry very different cold-chain and cost exposure,
and you cannot tell which without written carrier confirmation. So never collapse
"via X" onto the clean direct lane. Instead:
- Map it to a **dedicated contingency route** named for the ambiguity, e.g.
  `<Origin> to <Dest> via <Via-port> — routing unresolved` (Category: Wartime
  contingency; Status: Investigating; Risk: High; Inland Transfer Required left
  **blank** = unresolved, not "No"). Do not group it with the clean direct route.
- Set `Inland Trucking` and `Genset on Inland Trucking` to **Not Confirmed**, drive
  **Cold Chain Risk to High**, and add the discharge / road-leg / genset / temperature
  questions to the follow-up. A carrier saying "on-carriage inclusive" does **not**
  resolve this — it doesn't confirm the discharge port, whether a road leg exists, or
  whether that leg is genset-equipped and temperature-monitored.
- Treat a reefer as having **no inland leg** (genset `Not Applicable`) only when the
  carrier **explicitly** confirms direct discharge with the buyer collecting ex-quay.
  Silence is not confirmation.

### Step 5 — Preview and ask for approval (the gate)

Show the fully-mapped record field by field, the completeness score, cold-chain risk,
competitive position, the MISSING list, and the critical-risk flags — then **stop and
ask**: write to Production, edit something first, or keep as a dry run. Set the
conceptual `Quote Stage` to `Parsed / Awaiting Approval`. Do **not** write. Do **not**
create Route/Provider records. This is the default end state of every run unless and
until Gareth approves.

If Gareth's message itself contained an explicit write instruction ("write it",
"commit it", "save it to Airtable, no need to preview"), you may treat that as the
approval and proceed to Step 6 — but still show the mapped record in your response so
the write is auditable. Ambiguity ("log this quote") is **not** approval; preview.

### Step 6 — Write (only after approval)

On approval: search-or-create the Route and Freight Provider records, then write the
Freight Quotes record with `create_records_for_table` using the field map in
`references/airtable-schema.md`. Currency columns take **numbers only** — a
percentage ("0.3% of CIF") or "at cost" goes to Notes, not a fake number. Pack
everything without a dedicated column into the structured Notes block. List every
`MISSING` field in `Missing Information`. Set `Quote Stage`:
- `Written to Production` once committed (the normal case),
- `Expired` if the validity date has already passed,
- `Awaiting Clarification` is for the carrier-status sense (critical gaps + follow-up
  pending) — note it in the summary; the committed record's stage is still
  `Written to Production`.
Then confirm the new `rec…` id back to the user.

### Step 7 — Summarise

End with the exact format in "Output format" below.

## Critical flags — never skip these

Five fields have caused real problems. Whenever any is `MISSING`/`Not Confirmed`, call
it out explicitly in the summary (not just buried in a list):

1. **War risk surcharge** — wartime quotes that omit it hide ~USD 3,500–4,000/reefer.
   Silence is not INCLUSIVE; mark MISSING.
2. **Destination charges** — routinely excluded under CFR; can swing landed cost hard.
3. **Inland trucking cost** — the road leg from discharge port to Dubai.
4. **Genset on inland trucking** — for **any sea reefer quote**, if genset is not
   explicitly confirmed, set it `Not Confirmed`, drive Cold Chain Risk to High, add
   "genset confirmation" to the follow-up, and say so loudly. Single biggest
   cold-chain risk and the most frequently omitted item. Never let a reefer quote pass
   as "complete" with genset unconfirmed. If the routing is worded "via [port]", the
   inland leg's very existence is also unconfirmed — mark inland trucking Not Confirmed
   too and apply the Step 4 routing-ambiguity rule.
5. **Insurance** (marine and/or road) — spoilage liability over a 50–60 day wartime
   transit and the inland haul.

Always surface the **validity / expiry date** prominently. If it's expired or expires
within a few days, lead with that and set Quote Stage accordingly.

## Output format

After preview (default) or after writing, return exactly this shape:

```
Quote captured [PREVIEW — not written | WRITTEN rec…]: [Carrier] — [Route] — [method]
Rate: [base + original currency] = [AUD] (FX [rate], [date]); freight-only est: [AUD]
Validity: [expiry]  ⏳ [expires in N days / EXPIRED / none stated]

Completeness: [NN]% (critical X/9, standard Y/11)
Cold chain risk: [Low/Medium/High/Unknown — or n/a for air/sea-dry]
Competitive: [Cheapest known / Within range / Above range / Cannot determine]

✅ Known fields: [count]
⚠️ MISSING / unconfirmed: [comma-separated list]
🚩 Critical gaps: [any of war risk / destination / inland trucking / genset /
   insurance that are missing — or "none"]

Recommended action: [specific, named follow-up — e.g. "Email Stuart Taylor at MSC
   (stuart.taylor@msc.com): request destination charges + confirm genset on the
   inland leg"]

Pricing scenario ready: [Yes / No — blocked on X]

➡️ Write this to Production? (yes / edit first / keep as dry run)
```

- "freight-only est" = AUD sum of the freight-side costs you actually have; state it
  as an estimate and name what's excluded because it was MISSING. Never present it as
  final if critical gaps exist.
- "Pricing scenario ready" is **Yes** only if none of the five critical fields are
  missing and the quote is in validity; otherwise **No — blocked on [list]**.
- Drop the final approval line once the record has been written; replace it with the
  `rec…` id and the Quote Stage you set.

## Quick reference

- `references/airtable-schema.md` — base/table/field IDs (incl. the 7 new fields),
  select options, write recipe, Notes-block template.
- `references/routes-and-providers.md` — the 5 canonical routes (with create
  payloads), known carriers + contacts, wartime cost context.
- `references/scoring.md` — completeness %, cold-chain risk, competitive-position rubrics.
