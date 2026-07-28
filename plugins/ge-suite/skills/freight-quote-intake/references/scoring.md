# Scoring, cold-chain risk & competitive position

The three judgements the skill adds on top of raw extraction. All three are
**derived only from what the quote actually states** — same discipline as the rest
of the skill. A field is "known" if it has a real value OR a resolved state
(`EXCLUDED`, `INCLUSIVE`, `Not Applicable`). A field is "unknown" if it is `MISSING`
or `Not Confirmed`. Only genuine unknowns cost points / raise risk.

## 1. Quote Completeness % (field `fldESahiKp62hbOl3`)

Weighted: critical fields are worth 2 points, standard fields 1 point. Score =
`round(100 * earned / max_possible)`. Compute the denominator from the fields that
*apply* to this quote (so air freight is not punished for having no genset), then
show the breakdown so the number is auditable.

Critical fields (2 pts each):
- Freight base rate
- Route (maps to a canonical route, or routing is fully specified)
- Destination charges (a value, or a resolved EXCLUDED with whose-account stated)
- Insurance (marine; a value or resolved EXCLUDED)
- War risk surcharge (a value or resolved INCLUSIVE/EXCLUDED — silence ≠ resolved)
- Transit time
- Genset on inland trucking — **sea reefer only**; drop from the pool for air / sea-dry / port-to-port with no inland leg confirmed by the carrier. A "via [port]" quote is not confirmation: keep genset and inland trucking in the pool as Not Confirmed
- Inland trucking cost (a value or resolved — only when an inland leg exists)
- Quote validity / expiry date

Standard fields (1 pt each, count only those that apply):
- Origin charges
- Bunker / fuel surcharge
- Customs / duties
- Demurrage / detention free time
- Empty-container return responsibility
- Reefer plug availability at discharge (reefer only)
- Incoterms
- Container type / air weight tier
- Contact email
- Commodity restrictions
- Transhipment / routing detail

Worked example (illustrative — always compute from the actual quote; sea reefer, inland leg): 9 critical apply (18 pts) + 11 standard
(11 pts) = 29 max. If 6 critical known (12) and 7 standard known (7) → 19/29 →
**66%**. Show the line: `Completeness 66% (critical 6/9, standard 7/11)`.

## 2. Cold Chain Risk (field `fld9DOtJ7UBW0xfUC`: Low / Medium / High / Unknown)

Set this **only for sea reefer quotes**. Leave blank for air and sea-dry (no cold
chain on the water leg). Weigh six factors, each Good vs Bad-or-Unknown:

1. Genset confirmed on the inland leg — Good if `Confirmed`; **Bad if Not Confirmed**; N/A only if the carrier explicitly confirms there is no inland leg (direct discharge, buyer collects ex-quay). A "via [port]" routing is NOT such confirmation: treat genset as Not Confirmed and this factor as Bad.
2. Inland trucking included & priced — Good if priced/included; Bad if MISSING while an inland leg exists.
3. Temperature monitoring confirmed — Good if stated; Unknown otherwise.
4. Reefer plug available at discharge — Good if stated; Unknown otherwise.
5. Port congestion / transit exposure — Good if transit is short and the lane is clear; Bad if transit > ~55 days or the lane is congestion-prone (Khor Fakkan / via Colombo).
6. Carrier accepts liability for temperature excursion — Good if stated; Bad/Unknown otherwise (usually excluded).

Classify (lean conservative — this protects 22-tonne reefer loads):
- **High** — genset Not Confirmed on a route that has an inland leg, OR carrier explicitly excludes temp-excursion liability with ≥2 other factors Bad/Unknown, OR ≥4 of the six factors Bad/Unknown.
- **Medium** — genset Confirmed (or no inland leg) but 1–3 other factors Bad/Unknown.
- **Low** — every applicable factor Good.
- **Unknown** — the quote doesn't even reveal whether there's an inland reefer leg, so genset applicability can't be judged. Flag for clarification rather than guessing.

The default for a sea-reefer quote that is silent on genset is **High**, not Unknown.
Silence on the single biggest cold-chain risk is itself the risk.

## 3. Competitive Position (field `fldHLobBluphYRffI`)

Compare this quote against quotes already in the Freight Quotes table for the
**same route and method**. Search the table first (`search_records` / filter on
Route + Air-or-Sea). Compare on the AUD freight-side figure you actually have
(base + war risk, both in AUD).

- **Cannot determine** (default) — fewer than one valid comparator on the same lane, OR any critical charge missing on this quote (you can't fairly rank an incomplete quote).
- **Cheapest known** — comparable AUD total is the lowest among known quotes on the lane.
- **Within market range** — within ~10% of the cheapest known.
- **Above market range** — more than ~10–15% above the cheapest known.

When in doubt, **Cannot determine**. A confident ranking built on missing charges
misleads exactly when it matters.
