# Platform Data Protocol

The goal is one booking-level normalized ledger that supports every government return.

## OwnerRez - both accounts

For the requested filing period, gather/export enough current data to identify:

- booking/reservation identifier
- property
- booking status
- arrival/departure
- booking channel/source
- rent
- cleaning
- pet fee
- damage protection/deposit
- required host/service fees
- optional fees
- refunds/credits
- taxes collected
- tax line names/rates where available
- total guest charges

Preserve original exports. Do not edit source CSVs in place.

## Airbnb - both accounts

Gather current-period transaction/tax evidence sufficient to determine, by listing/property and tax type:

- gross booking receipts relevant to filing
- taxes collected
- taxes remitted by Airbnb
- tax jurisdiction/type when available
- reservation identifiers allowing tie-out to OwnerRez
- refunds/adjustments

Do not infer county TDT remittance from state sales-tax remittance. Establish each tax type separately.

## Vrbo - both accounts

Gather current-period transaction/tax evidence sufficient to determine, by listing/property and tax type:

- gross booking receipts relevant to filing
- taxes collected
- taxes remitted by Vrbo, if any
- taxes passed through to the business
- reservation identifiers allowing tie-out to OwnerRez
- refunds/adjustments

Vrbo treatment may differ by tax/jurisdiction and historical period. Use current evidence.

## Direct/manual bookings

OwnerRez/direct records must identify all tax-bearing charges and taxes collected. These are usually the highest-control transactions and require full tax-base reconciliation.

## Normalized ledger fields

At minimum create:

| Field | Purpose |
|---|---|
| booking_id | cross-system tie-out |
| property | account mapping |
| entity | filing ownership |
| county_state | jurisdiction |
| platform_account | source account |
| channel | Airbnb/Vrbo/direct/etc. |
| filing_period | return assignment |
| rent | tax base component |
| cleaning_fee | tax base component |
| pet_fee | tax base component |
| other_required_fee | tax base component |
| optional_or_deposit | exemption/non-tax review |
| taxable_base_state | Florida/Utah sales-tax base |
| taxable_base_county_tdt | county/transient-room base |
| marketplace_state_remit | marketplace exclusion evidence |
| marketplace_local_remit | marketplace exclusion evidence |
| business_tax_collected | reconciliation |
| expected_tax | rate calculation |
| variance | control |
| evidence_source | audit trail |

## Reconciliation tolerance

Do not silently round away unexplained differences. Use exact source totals to cents. Any rounding difference should be documented and attributable to portal/system calculation mechanics.
