# Learning Log

Durable, verified procedural learnings from real filing cycles. Identifiers, entity names,
property names and amounts are deliberately omitted — the lessons are what transfer.

Add only durable procedural facts or user-confirmed mappings. Never copy secrets here.

## Identifier integrity

- **Historical account numbers are the lowest-confidence tier and are often simply wrong.** In one
  cycle, all three county tourist-tax account numbers held in a registry were incorrect — the live
  portal showed 7-digit numbers where the registry held 6-digit ones, and the differences were
  *not* a single consistent transformation. They were bad notes, not inferable transcription slips.
  **Read county account numbers off the live portal every period.**
- Never retype a long government account number from memory when a registry value exists.
- Never merge two similar account numbers or "correct" a digit by intuition.
- Where a historical value has been superseded, record the deprecated number explicitly so it
  cannot silently reappear.
- A portal's account or location label may name the **entity** rather than the **property**. The
  certificate number is the authoritative join, not the display name.
- Cross-agency name mismatches are common: the same property can appear under an operating company
  at the state level and under an individual's name at the county level. Filing is unaffected;
  do not "fix" it from a filing workflow.

## Credentials are scoped per entity, not per portal

- State guest-filing paths may authenticate on a **per-entity** identifier (such as a business
  partner number) plus the certificate. One such identifier can cover several certificates for the
  same entity, but never crosses entities.
- County portals may require a **separate login per entity**. If an expected account is missing from
  an account list, treat it as a credentials-scope issue before concluding the account is closed —
  check every status filter first, including inactive.
- Budget for one authentication hand-off per entity per portal.

## Rate sources

- **A "current" form URL may serve the prior year.** Always confirm the calendar year printed in the
  document header before using a rate from it. Year-specific filenames are safer.
- **For a county-administered tax, the county is authoritative over the state's summary table.** One
  state form listed a county rate a full point higher than the county itself published, and that
  form self-disclaimed: not all counties notify the state of rate changes. Resolve to the county
  ordinance, then confirm against the portal's own computation at entry.
- Rates can change mid-year and mid-quarter. Re-verify every period against the period being filed,
  not against today.
- A filing template that carries its own rate formula is a useful independent confirmation of the
  rate you believe applies.

## Marketplace treatment differs by platform — never assume

- Two marketplaces in the same jurisdiction can have **opposite** postures. One may remit state tax
  and surtax while passing local occupancy tax through to the host; another may remit nothing at
  all. Establish each platform, each tax type, each period, from evidence.
- **State-tax remittance by a marketplace does not imply local occupancy-tax remittance.** Some
  counties state in writing that platforms do not remit their tax and the owner must.
- **Ratio test for proving posture without a tax-type breakdown:** divide a listing's
  platform-remitted tax by its pass-through tax. If the result lands exactly on
  `(state% + surtax%) / local%` for that jurisdiction, it proves which taxes the platform handles.
  Different jurisdictions produce distinctly different ratios, so the test also confirms which
  jurisdiction a listing sits in. It survives misaligned PDF table columns.
- Where a platform is **not** in the payment path — because a property-management system processes
  payment — its own tax report may show zero taxes paid on its behalf across all periods. That
  absence is meaningful evidence, but record it as evidence of absence, not as a positive
  declaration.

## Cancelled bookings are a tax risk in two distinct ways

1. **Cancel-and-rebook pairs retain full charges and tax on the cancelled row.** Filing an export
   as-exported double-counts the revenue, because the replacement booking already carries it.
   Exclude the cancelled row.
2. **A cancelled booking with a retained, unrefunded charge is a taxable event that the PMS may
   record with zero tax.** Where a forfeited deposit or prepayment guaranteed the guest the right to
   occupy, it is generally taxable even though nobody stayed. Marketplaces often tax these correctly
   while the PMS does not flag them.
   - Test: `total charged > 0`, `total refunded = 0`, status cancelled → check for forfeiture.
   - A **released** security deposit is not part of the base; only *retained* charges are.
   - For a marketplace booking, state tax may fall to the platform while the **local occupancy tax
     still falls to the business**.

## PMS report controls

- Report options that **default to excluding** zero-tax bookings hide exactly the exception rows
  that matter — marketplace-collected and mis-mapped bookings. Enable them.
- A PMS "taxable charges" column can **exceed the base it actually taxed**. Reconcile the two; never
  assume the tax figure implies the base.
- Where expected tax differs from collected tax: preserve the verified base, file what is correct
  under current rules, log the over/under-collection separately, and **do not change tax settings
  during a filing run**. Open a separate authorised audit afterwards.
- Watch for **duplicate tax lines for the same tax** — for example a channel-specific variant
  alongside the standard line — firing inconsistently, including on bookings from the wrong channel.
  Sum them for the return; the split is a mapping defect, not two different taxes.

## Reconciliation technique

- Marketplaces report on a **payout basis**; a PMS ledger may be on an **arrival or accrual basis**.
  Expect a timing variance and identify it booking-by-booking rather than absorbing it.
- A residual gap *after* timing is explained is a genuine base difference and worth investigating —
  that is how forfeited-charge revenue surfaces.
- Classify every variance: explained and documented, open and unexplained, material, immaterial, or
  needing government/CPA verification. Do not silently round away a difference.

## Template-upload filings

Some returns are filed by uploading an official spreadsheet rather than typing into a form.

- **Write literal computed values, not formulas.** Libraries that write spreadsheets do not evaluate
  formulas, so formula cells upload empty and the portal rejects the file — or worse, accepts a
  zero. Paste values.
- **Carry full precision into the value cells** and let the portal's own total round once. Rounding
  each row first can shift the total by a cent against an approved figure.
- **Preserve the workbook structure exactly.** Never invent a row for a property the authority did
  not include; if one is missing, stop the upload path and resolve the account/property list.
- **Verify each row's account number and address before writing figures to it.** Never rely on row
  order alone.
- Check the **required file format**. At least one authority accepts only legacy `.xls` and rejects
  `.xlsx`, which rules out the common Python writers.
- A template that arrives pre-populated with the authority's own property list is also the
  authoritative answer to "which properties are on this account".

## Portal behaviour

- **Filing portals fail mid-transaction.** After any error, **verify the row or return status before
  re-filing** — never re-submit blind on a live tax account. A well-behaved portal rolls the
  transaction back cleanly, but that must be confirmed, not assumed.
- Instability is not limited to multi-account submissions; single-row filings fail too.
- Some portals require a full log-off, hard refresh and log-back-in between filings. Where an
  operator has learned such a workaround, follow it.
- **Navigating to a login URL is not proof of a logged-out state** — a portal may silently serve the
  authenticated view of a *different* account. Verify the page is genuinely signed out, and which
  account is signed in, before handing over for authentication.
- Portal **submission and activity logs may be profile-scoped, not account-scoped**. Work done by
  another authorised user is invisible in your own view. When a record looks contradictory, check
  whether another user with access could have done it before concluding anything.
- The activity log is also how you **prove what a session did or did not do** — valuable when a
  read-only walkthrough passes through a link labelled "view or amend".
- Automated element-finding can **mis-attribute a control to the wrong row** in a multi-row filing
  table. Resolve controls by element ID tied to the account number, not by row position or label.
- A payment marked "in process" or "scheduled" is **accepted, not cleared**. Record scheduled and
  cleared separately, and confirm the debit actually lands.

## Fees and allowances

- Collection allowances are typically a small percentage capped at a low ceiling, so larger returns
  hit the cap and the allowance stops scaling. Let the portal compute it rather than typing it.
- Allowances are usually conditional on **electronic filing and electronic payment and timeliness**.
- Payment **convenience fees vary by portal and by method**. One portal charged a flat sum for ACH
  and a percentage for card; on a four-figure payment the card route cost far more for identical
  settlement. Prefer ACH, and record tax and fee separately.
- Some portals charge no fee at all. Do not assume either way.
- Card and e-check payments are often **non-cancellable once made**, unlike scheduled state debits.

## Cadence

- **Do not assume one jurisdiction's cadence implies another's.** A monthly state filing does not
  mean a second state's quarterly account is due. Check the portal for an **open period** before
  gathering data.
- A quarterly period may not exist in the portal at all until the quarter closes.
- A period showing "processed" on a dashboard can still carry a **pending amendment** visible only
  when the return itself is opened. Open the return before treating a period as settled.

## Zero and not-due periods

- A zero-tax period usually still requires a return. Verify per jurisdiction.
- "Not due" is a legitimate closing state and is different from "unfiled". Document which one
  applies, with the evidence that establishes it.
