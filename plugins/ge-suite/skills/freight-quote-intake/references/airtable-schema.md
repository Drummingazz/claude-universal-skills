# Airtable schema & write recipe — Global Exporters OS Production

Everything you need to read from and write to the base. Field IDs are stable; use
them as the keys when calling `create_records_for_table` / `update_records_for_table`
(the API requires field **IDs**, not names, as keys).

## IDs

- Base: `appxVfr0LXoZ8ASCL`  (name: "Global Exporters OS Production")
- Freight Quotes table: `tblZPX36hhg7ZLipU`
- Routes table: `tblukfwxEB71MPY05`
- Freight Providers table: `tblCTQLd3LFkUC2ma`

## Freight Quotes — field map

Write each quote value into its dedicated column. Currency columns take **numbers
only** (no "$", no commas). Set the `Currency` text field to say which currency the
stored amounts are in (usually "USD" for sea freight base rate, but state the mix in
Notes).

| Field name | Field ID | Type | Notes / select options |
|---|---|---|---|
| Carrier | `fld7D5dxtyKBVZRCi` | singleLineText (primary) | Carrier / forwarder name |
| Freight Provider | `fldCBgiqHydjz3Qsw` | link → Freight Providers | array of record IDs |
| Route | `fldpF20VKLie6Xcpr` | link → Routes | array of record IDs |
| Origin Port | `fldkiH3JOFUxoSTWr` | singleLineText | usually "Adelaide" |
| Destination Port | `fld96wQi23RtZHpP1` | singleLineText | Jebel Ali / Khor Fakkan / Sohar / Salalah / Fujairah |
| Transhipment Port | `fldTIikFjgvpNpcfz` | singleLineText | e.g. Colombo, Fujairah |
| Air or Sea | `fldDrgfIeJ0ou9Xqm` | singleSelect | `Air`, `Sea` |
| Container Type | `fldInp7seD7ffIIzj` | singleLineText | "20ft reefer", "40ft reefer", or air weight tier |
| Reefer Capability | `fld736W0xNvfBqavf` | singleSelect | `Yes`, `No` |
| Commodity Restrictions | `fldo0xt0nY1lnFlGr` | multilineText | |
| Transit Time | `fldipToirTvDPmak1` | singleLineText | e.g. "~62 days incl. congestion" |
| Freight Cost | `fldrgWVwhSbl6tPpV` | currency | ocean/air **base** rate (number) |
| Origin Charges | `fldzBWB6lPG1dOi4V` | currency | total; itemise in Notes |
| Destination Charges | `fldoC2X2YPfPKcz4a` | currency | |
| Inland Trucking | `fldbVKDwe0FTLwerI` | currency | |
| Insurance | `fldh5w5s5yBnSOuYU` | currency | marine insurance (number). Road insurance → Notes |
| War Risk Surcharge | `fldPqpTkKQEgQWinc` | currency | |
| Customs/Duties | `fldX2z3pswkuTn2w6` | currency | |
| Bunker/Fuel Surcharge | `fldP3QCDOpa1Bdeab` | currency | BAF / EBS / emergency fuel |
| Currency | `fldIFpl9Wd1C7wBFN` | singleLineText | dominant quote currency, e.g. "USD" |
| AUD Conversion Rate (LEGACY) | `fldqTIcgVUhiljPUY` | number (precision 0) | DEPRECATED — rounds to integer. Leave blank; use `FX Rate Used` instead |
| Quote Valid Until | `fldlXdbPeGly4h6eu` | date | `YYYY-MM-DD`. Expiry — surface prominently |
| Genset on Inland Trucking | `fldOBN2wQAd0edm2Z` | singleSelect | `Confirmed`, `Not Confirmed`, `Not Applicable` |
| Incoterms | `fld7nQ3wohHXEvyNQ` | singleLineText | CFR / FOB / CIF / DAP / DDP |
| Contact Name | `fldiBdBgyfObwU4Pf` | singleLineText | |
| Contact Email | `fldoOpLXyLmuBB6ft` | email | |
| Quote Status | `fldrBjYQU4i71GhHL` | singleSelect | `Draft`,`Requested`,`Received`,`Under Review`,`Approved`,`Rejected`,`Pending`,`Confirmed` |
| Confidence Level | `fldkJdep9V8MTAyVb` | singleSelect | `High`,`Moderate`,`Medium`,`Low` |
| Date Received | `fldjwHYPO06TvAzE5` | dateTime | quote date, ISO 8601 e.g. `2026-06-01T00:00:00.000Z` |
| Last Follow-up | `fldDvJjHfQM4Zc7WJ` | dateTime | leave blank on intake |
| Missing Information | `flda8n7jVTrzWidye` | singleLineText | comma-separated list of MISSING fields |
| Notes | `fldJnXt5eAsL4ZV8z` | multilineText | structured block (template below) |
| **Freight Cost (AUD)** | `fldWgarGiVRqgA0au` | currency | base freight converted to AUD (number). Original stays in Freight Cost |
| **FX Rate Used** | `fldsbGspltPyWFwTy` | number (precision 4) | exact rate used, e.g. 1.3917. AUTHORITATIVE FX store |
| **FX Rate Captured At** | `fldLp32Tbj5CZIo9A` | singleLineText | e.g. `2026-06-01 USD to AUD mid-market` — locks comparability |
| **Quote Completeness %** | `fldESahiKp62hbOl3` | number (0-100) | weighted score (see scoring.md); write integer 0-100 |
| **Cold Chain Risk** | `fld9DOtJ7UBW0xfUC` | singleSelect | `Low`,`Medium`,`High`,`Unknown` — sea reefer only; blank for air/sea-dry |
| **Competitive Position** | `fldHLobBluphYRffI` | singleSelect | `Cheapest known`,`Within market range`,`Above market range`,`Cannot determine` |
| **Quote Stage** | `fld1SzOgRb2jQkpOV` | singleSelect | `Parsed / Awaiting Approval`,`Awaiting Clarification`,`Ready for Comparison`,`Written to Production`,`Superseded`,`Expired` |

Link fields that exist but are normally left blank on intake: Deals/Opportunities
`fld6PjGyeE9lB4CvL`, Alerts `fldLwJLX49qvON6mI`, Pricing Scenarios `fldPj02B63GA36boH`,
Tasks `fldL3P6ZIOBcIPL3J`, Documents `fldMNFoIlUubxHw2v`.

### Where each spec field goes

Dedicated column: carrier, contact name, contact email, quote date (Date Received),
expiry (Quote Valid Until), method (Air or Sea + Reefer Capability), container type,
ports, transhipment, base rate, origin/destination charges, war risk, bunker,
inland trucking, marine insurance, customs, transit time, commodity restrictions,
Incoterms, genset, currency, conversion rate.

Structured **Notes block** (no dedicated column): routing detail beyond
transhipment, **road insurance**, demurrage/detention terms + free time,
empty-container return responsibility, reefer plug availability, exclusions/
conditions, the AUD conversion line, and any extra notes.

### Notes block template

```
--- QUOTE DETAIL (Freight Quote Intake, captured <date>) ---
Routing: <full routing / multimodal detail, or MISSING>
Origin charges breakdown: <itemised list, or "total only" / MISSING>
Road insurance: <value/terms, or MISSING>
Demurrage / detention: <free time + daily rate, or MISSING>
Empty container return: <responsibility/location, or MISSING>
Reefer plug at discharge port: <available / not / MISSING>
Exclusions & conditions: <text, or "none stated">
Clauses & fine print: <every clause, subclause, surcharge/adjustment term, validity or revision clause, liability, force majeure, and any disclosure printed below or after the quote, quoted verbatim; or "none stated">
Currency conversion: <e.g. USD 12,500 = AUD 19,000 at USD1=AUD1.52, 1 Jun 2026 — ASSUMPTION>
Other notes: <freeform, or none>
```

## Routes — field map (for creating a route reference record if missing)

| Field name | Field ID | Type | Select options |
|---|---|---|---|
| Route Name | `fldIDktsHrzPSdrIx` | singleLineText (primary) | |
| Route Category | `fldtYdTH3LDojr4Ck` | singleSelect | Post-war standard, Wartime contingency, Mainline, Feeder, Regional, Intermodal, Direct |
| Origin Country | `fldoqaWoDhq323w3x` | singleLineText | |
| Origin Port/Airport | `fld6a3NW21LIp3sli` | singleLineText | |
| Transhipment Port | `fldAp4NFqrBBhWaGi` | singleLineText | |
| Destination Country | `fldRKej4f6OFdBTFn` | singleLineText | |
| Destination Port/Airport | `fldW1sT63ur3fQATb` | singleLineText | |
| Inland Transfer Required | `fld4ypLLN3ZU9dtja` | singleSelect | Yes, No |
| Inland Transfer Destination | `fldeRBId9CjXUWTRs` | singleLineText | |
| Air or Sea | `fld970xEH9dYVabwQ` | singleSelect | Air, Sea |
| Reefer Suitability | `fldzy2WPz5TEUm3Pj` | singleSelect | Yes, No |
| Current Operational Status | `flds7dL4c91771dif` | singleSelect | Operational, Blocked, Investigating |
| Commercial Confidence Level | `fldHfOEXHoHq7MZSC` | singleSelect | High, Moderate, Medium, Low |
| Risk Level | `fldj9SS4ew5EXH1jT` | singleSelect | High, Medium, Low |
| Estimated Transit Time | `fld2THehP93WjQtjF` | singleLineText | |
| Notes | `fldWgujl00KfPePVG` | multilineText | |

## Freight Providers — field map

| Field name | Field ID | Type |
|---|---|---|
| Provider Name | `fldMEj9fn2ytL24Nt` | singleLineText (primary) |
| Contact Details | `fldJEdZJ0yjdinnqM` | singleLineText |
| Service Notes | `fld4ng0tcda2Sscg8` | multilineText |

## Linking recipe (Route & Provider)

1. **Search first** so you don't create duplicates: `search_records` on the table
   (e.g. table "Routes", query the route name; table "Freight Providers", query the
   carrier). Or `list_records_for_table`.
2. If a matching record exists, grab its `rec…` id.
3. If not, create it with `create_records_for_table`, then read the returned `rec…`
   id from the response.
4. On the Freight Quotes record, set the link field to an **array** of record IDs:
   `"fldpF20VKLie6Xcpr": ["recXXXXXXXXXXXXXX"]` (Route),
   `"fldCBgiqHydjz3Qsw": ["recYYYYYYYYYYYYYY"]` (Freight Provider).

## Write recipe — example create_records_for_table call

```json
{
  "baseId": "appxVfr0LXoZ8ASCL",
  "tableId": "tblZPX36hhg7ZLipU",
  "records": [{
    "fields": {
      "fld7D5dxtyKBVZRCi": "Seaway Logistics",
      "fldiBdBgyfObwU4Pf": "Nathan Borg",
      "fldoOpLXyLmuBB6ft": "nathan.borg@seaway.com.au",
      "fldCBgiqHydjz3Qsw": ["recPROVIDERID000"],
      "fldpF20VKLie6Xcpr": ["recROUTEID000000"],
      "fldkiH3JOFUxoSTWr": "Adelaide",
      "fld96wQi23RtZHpP1": "Jebel Ali",
      "fldTIikFjgvpNpcfz": "Fujairah",
      "fldDrgfIeJ0ou9Xqm": "Sea",
      "fldInp7seD7ffIIzj": "20ft or 40ft reefer (20RE/40RE)",
      "fld736W0xNvfBqavf": "Yes",
      "fldrgWVwhSbl6tPpV": 12500,
      "fldzBWB6lPG1dOi4V": 309.50,
      "fldIFpl9Wd1C7wBFN": "USD (freight) / AUD (origin)",
      "fldWgarGiVRqgA0au": 18625.00,
      "fldsbGspltPyWFwTy": 1.4900,
      "fldLp32Tbj5CZIo9A": "<capture date> USD to AUD mid-market",
      "fldESahiKp62hbOl3": 72,
      "fld9DOtJ7UBW0xfUC": "High",
      "fldHLobBluphYRffI": "Cannot determine",
      "fld1SzOgRb2jQkpOV": "Written to Production",
      "fldlXdbPeGly4h6eu": "2026-06-15",
      "fldOBN2wQAd0edm2Z": "Not Applicable",
      "fld7nQ3wohHXEvyNQ": "CFR",
      "fldrBjYQU4i71GhHL": "Received",
      "fldkJdep9V8MTAyVb": "High",
      "fldjwHYPO06TvAzE5": "2026-05-XXT00:00:00.000Z",
      "flda8n7jVTrzWidye": "Destination charges, Marine insurance, Road insurance, Inland trucking",
      "fldJnXt5eAsL4ZV8z": "--- QUOTE DETAIL ... ---\nExclusions: marine/road insurance, destination charges, customs, taxes\n..."
    }
  }]
}
```

(The values above are illustrative of the **mapping**, not numbers to copy — always
use the real figures from the actual quote in front of you.)
