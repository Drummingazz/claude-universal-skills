# Canonical routes & known freight providers

Use this to (a) decide which Route a quote maps to, (b) create a Route reference
record if it doesn't exist yet, and (c) create/identify the Freight Provider with
real contact details. Field IDs for the create call are in `airtable-schema.md`.

All values below come from confirmed project intelligence (1 June 2026). They are
legitimate reference data. Numbers in a *quote* still override these — these are
defaults for the **route reference record**, not for the quote's own figures.

## The five canonical routes

Match on the quote's **port of discharge** — but apply the routing-ambiguity rule first.

**"via [port]" is not a clean direct discharge.** A quote that says "to Jebel Ali
**via Fujairah**" (or via Colombo, etc.) is *unresolved*: it could mean (1) discharge at
the via-port + bonded/road land bridge onward, (2) a vessel call there then onward by
sea, or (3) transhipment onto another vessel. Do **not** map it onto the clean direct
lane (route 1) and do **not** assume "no inland leg." Create a dedicated
`… via <port> — routing unresolved` contingency route (Wartime contingency /
Investigating / Risk High; Inland Transfer Required left blank), set Inland Trucking +
Genset to Not Confirmed, Cold Chain Risk High, and put the discharge / road-leg / genset
/ temperature questions to the carrier. Collapse to route 1 only when the carrier
confirms direct Jebel Ali discharge in writing.

Match on the quote's **port of discharge**:

### 1. Adelaide to Jebel Ali
- Port of discharge: **Jebel Ali** (Dubai's main port — inside UAE, simple customs)
- Air or Sea: Sea · Reefer Suitability: Yes
- Transhipment: often Fujairah or Colombo · Inland Transfer Required: No
- Route Category: Wartime contingency · Status: Operational
- Commercial Confidence: High · Risk Level: Medium · Est. transit: ~50–58 days
- Notes: Seaway-confirmed CFR reefer route. Discharge inside UAE = simplest customs,
  no Oman cross-border. Preferred when available. Use this lane only when the carrier confirms direct Jebel Ali discharge in writing; a quote worded "via Fujairah/Colombo" is routing-unresolved, not this route.

### 2. Adelaide to Fujairah to Dubai
- Port of discharge: **Fujairah** (UAE east coast)
- Air or Sea: Sea · Reefer Suitability: Yes
- Inland Transfer Required: Yes → Dubai (~120 km truck)
- Route Category: Wartime contingency · Status: Operational
- Commercial Confidence: Moderate · Risk Level: High · Est. transit: ~58 days
- Notes: Inside UAE = simple customs, short ~120 km haul. **High-risk / drone-threat
  zone.** Seaway-confirmed routing.

### 3. Adelaide to Khorfakkan to Dubai
- Port of discharge: **Khor Fakkan** (a.k.a. Khorfakkan, UAE east coast)
- Air or Sea: Sea · Reefer Suitability: Yes
- Inland Transfer Required: Yes → Dubai (~150 km truck)
- Route Category: Wartime contingency · Status: Operational
- Commercial Confidence: Moderate · Risk Level: Medium · Est. transit: ~62 days
- Notes: Most common route; **congested — adds ~2 weeks** after ocean transit.
  Inside UAE = simple customs. MSC-confirmed (Adelaide→Colombo→Khor Fakkan).

### 4. Adelaide to Sohar to Dubai
- Port of discharge: **Sohar** (Oman)
- Air or Sea: Sea · Reefer Suitability: Yes
- Inland Transfer Required: Yes → Dubai (~400 km truck, Oman→UAE cross-border)
- Route Category: Wartime contingency · Status: Operational
- Commercial Confidence: Moderate · Risk Level: Low · Est. transit: ~55 days
- Notes: Less congestion (~38–40 days water), but **complex cross-border customs**
  Oman→UAE. MSC-confirmed (Adelaide→Colombo→Sohar).

### 5. Adelaide to Salalah to Dubai
- Port of discharge: **Salalah** (Oman)
- Air or Sea: Sea · Reefer Suitability: Yes
- Inland Transfer Required: Yes → Dubai (~1,100 km truck, Oman→UAE cross-border)
- Route Category: Wartime contingency · Status: Investigating
- Commercial Confidence: Low · Risk Level: Low (sea) · Est. transit: ~52 days
- Notes: "Father's model." **Genset risk on the ~1,100 km / ~18-hour inland haul is
  the single biggest cold-chain concern on any route** — confirm genset before
  trusting this route for reefer.

If a quote's discharge port isn't one of these (or is air freight to DXB), don't
force a match — leave Route blank and flag it in the summary. Air freight to Dubai
(DXB) has no canonical sea route; note it and leave Route unlinked unless an air
route record already exists.

## Known freight providers (create with these contacts if missing)

| Provider | Contact Details | Service Notes |
|---|---|---|
| Seaway Logistics | Nathan Borg, Procurement Mgr Export Seafreight — nathan.borg@seaway.com.au, +61 407 661 982 / +61 3 9014 8106. Air: Ryan Harrowfield, Perishable Air Freight, ryan.harrowfield@seaway.com.au, 0434 993 403 | Reefer, UAE routing, door-to-door, export docs. Air via Emirates SkyCargo. Confirmed quote received. |
| MSC | Stuart Taylor — stuart.taylor@msc.com | Direct carrier. Confirmed Adelaide→Colombo→Khor Fakkan and →Sohar. Reefer pricing was pending. |
| CT Freight | CTADL@ctfreight.com (Jacob → Steve/Jordan) | Forwarder. Quote pending. |
| DHL | Hope Island contact | Valuable for produce preservation advice as well as freight. |
| Kuehne + Nagel | 07 3623 7900 | Escalated internally; follow up if no response. |
| Team Global Express / Toll | 13 18 43 (Hayley); Adelaide Air Express 08 7224 5922 / airexpressadl@teamglobalexp.com | Air express option. |
| CMA CGM / ANL | (already contacted) | Most active carrier for cold-chain via Oman multimodal. Don't re-contact unless following an existing enquiry. |
| Hapag-Lloyd | (contacted) | NOT suitable — no reefer on this route. Intelligence only. |
| COSCO | +61 3 8679 8888 | No answer; deprioritised. |

For an unknown provider not in this list, create the record from the contact details
in the quote itself.

## Wartime cost context (for sanity-checking, NOT for filling gaps)

- War risk surcharge per reefer: **USD 3,500–4,000** (carrier-dependent).
- Pre-war Adelaide→UAE reefer ~USD 4,000–6,000; wartime all-in ~USD 10,500–13,900.
- Seaway's USD 12,500 ocean rate is mid-range / competitive for wartime.
- Most Western carriers (Maersk, Hapag-Lloyd, ONE, ZIM) restricted/suspended Gulf
  reefers; CMA CGM most active via Oman; MSC confirmed availability directly.

Use this only to judge whether a quoted number looks plausible and to phrase the
summary — **never** to backfill a MISSING figure with one of these ranges.
