# myTax field mechanics and the FY2024-25 worked outcome

Discovered during the real FY2024-25 lodgement (lodged 2026-07-16). Verify each mechanic still matches the current myTax before relying on it in a new year; the ATO changes the form.

## Field mechanics that cost real time

1. "Did you receive any personal services income?" Answer No when self-assessing as a PSB and reporting via "Business income or loss" (not "Personal services income") at Personalise return. Confirmed correct: the Small Business Income Tax Offset explicitly does not apply to income shown at Personal services income, so the path choice must be consistent all the way through.
2. Depreciation is entered in TWO places. "Deduction for certain assets" under Small business entity simplified depreciation (Other business and professional items) is only the disclosure breakdown. The actual deduction must also be entered in "Depreciation expenses, manually calculated" in the Net non-primary production expenses section, or myTax throws a validation error ("simplified depreciation amounts... are greater than depreciation amounts at Business income or losses"). Net income does not change, only which field holds the figure.
3. Reconciliation fields need manual re-entry even when the number exists elsewhere. "Remaining net non-primary production income or loss from business" does not auto-populate from "Net non-primary production income or loss from business this year," even with $0 in the investing and rental fields. Type the matching figure manually. The displayed running "Total" can show a stale $0 until the section fully saves; never copy that stale figure.
4. The net business income figure gets entered a THIRD time, into "Net small business income (from sole trading activities)" on the Small Business Income Tax Offset screen.
5. Rounding is per field, ATO standard (.00 to .49 down, .50 to .99 up), not on a final total.

## FY2024-25 worked outcome (lodged 2026-07-16)

- Taxable income $31,333.00: business $21,102 plus JobSeeker $10,231, both received with $0 tax withheld at source. That zero withholding is exactly why this year produced a bill rather than a refund; prior-year refunds came from employee-style PAYG over-collection, not a threshold difference.
- Tax on taxable income $2,101.28, less offsets $1,561.42 (government allowance beneficiary $635.00, low income earner $700.00, small business income $226.42), plus Medicare levy $411.10.
- Estimated amount payable: $950.95. Lodged.
- PAYG instalments check: automatic entry requires ALL THREE simultaneously: instalment income $4,000 or more, tax payable on the notice of assessment $1,000 or more, and notional tax $500 or more. Tax payable of $950.95 sat under the $1,000 line, which alone kept this return out of instalments. The $500 notional-tax threshold was not independently verified as year-specific; re-check if a future year lands over $1,000 payable. Confirm the instalment outcome against the actual notice of assessment once issued, since the myTax estimate can differ from the final figure.

## Full record

Every reclassification decision with Gareth's reasoning, and every correction made mid-session, is in the vault at Engines/GCE/FY2024-25-tax-return-fable-review-packet.
