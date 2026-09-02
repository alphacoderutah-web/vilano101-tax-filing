# Operating Rules

## Source-of-truth hierarchy

For high-impact filing decisions use:

1. Current live government portal
2. Current official government statute/rule/instructions/bulletin/FAQ or written agency communication
3. User-supplied government registration/notice documents summarized in `verified-tax-accounts.md`
4. Current filed-return/payment confirmations
5. Current-period OwnerRez exports
6. Current-period Airbnb tax/transaction reports
7. Current-period Vrbo tax/transaction reports
8. Direct/manual booking records
9. Payment processor/accounting records
10. Prior-period trackers and historical master-prompt notes
11. User recollection
12. General assumptions

If a current source conflicts with a lower-authority source, use the higher-authority source and log the conflict.

## Identifier integrity

- Never manually retype a long government account number from memory when a registry value exists.
- Compare the live portal's last digits/full certificate to `account-registry.yaml` before entering a return.
- If the portal shows an unexpected account number, stop and resolve the mapping before filing.
- Never merge two similar account numbers or "correct" a digit by intuition.
- A superseded certificate number that was corrected once is a permanent data-quality lesson: record the deprecated value explicitly so it cannot silently reappear.

## Tax-close principles

- Reconciliation is mandatory.
- Map: state -> county -> property -> ownership entity -> operating entity -> platform account -> channel -> tax type -> government filing account.
- Separate tax collected from tax remitted.
- Separate marketplace-remitted from business-remitted tax.
- Do not assume marketplace treatment from channel name alone.
- Preserve filing/payment evidence.
- Treat every filing/payment as audit-relevant.
- If zero tax is due, still verify whether a zero return is required.

## Deadline control

- Florida DR-15 current instructions: returns/payments are due on the 1st and late after the 20th of the following month; electronic payment initiation has an earlier practical cutoff specified by DOR. Verify the calendar every period.
- Flagler TDT current official guidance: due monthly on the 1st and delinquent after the 20th; timely online filing/payment may qualify for collection allowance. Verify current page/portal.
- For any account with prior penalty-waiver history, target completion at least 3 business days before the electronic deadline.
- Do not treat a filed return as timely paid until payment scheduling/confirmation is verified.

## Marketplace control

For each jurisdiction and tax type, create a current-period channel matrix:

| Channel | Tax type | Marketplace collected? | Marketplace remitted? | Business must report/remit? | Evidence |
|---|---|---|---|---|---|

No row may be marked `marketplace remitted` without current evidence or a verified durable platform/jurisdiction rule that applies to the period.

## OwnerRez mismatch rule

If expected tax differs from OwnerRez collected tax:

1. Preserve the verified taxable base.
2. Calculate what should be filed under current rules.
3. Log over/under-collection separately.
4. Do not change tax cards in the filing workflow.
5. Open a separate OwnerRez tax-setting audit task after filing if needed.

## Sensitive-data rule

Persist only non-secret tax account identifiers and operational mappings. Do not persist authentication or payment secrets.

## Risk levels

- `CRITICAL`: overdue/unpaid tax, audit/enforcement notice, known materially incorrect filing, large unexplained variance, portal access failure at deadline.
- `HIGH`: incorrect account mapping, material taxability uncertainty, prior penalty account near deadline, missing confirmation, repeated OwnerRez mismatch, possible amendment.
- `MEDIUM`: incomplete records, pending verification, immaterial unexplained variance, unclear platform mapping.
- `LOW`: fully reconciled routine item with current sources and confirmations.
