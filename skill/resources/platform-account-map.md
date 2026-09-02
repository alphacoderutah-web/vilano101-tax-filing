# Platform Account Map

**Template.** Populate from live browser access with **non-secret labels only**, then keep the
populated copy private.

Many portfolios run more than one account per platform. Record which is which, because the
property-to-account split is rarely obvious and is a common source of missed revenue.

## Property management system

| Account key | Non-secret account label | Entities/properties | Last verified | Notes |
|---|---|---|---|---|
| PMS-1 | UNMAPPED | | | |
| PMS-2 | UNMAPPED | | | |

## Airbnb

| Account key | Non-secret account label | Listings/properties | Last verified | Notes |
|---|---|---|---|---|
| AIRBNB-1 | UNMAPPED | | | |
| AIRBNB-2 | UNMAPPED | | | |

## Vrbo

| Account key | Non-secret account label | Listings/properties | Last verified | Notes |
|---|---|---|---|---|
| VRBO-1 | UNMAPPED | | | |
| VRBO-2 | UNMAPPED | | | |

## Things worth capturing

- **Channel-integration external IDs.** Most PMS/channel integrations stamp an external ID on the
  listing. That ID is the reliable join between a channel listing and its PMS property — far more
  reliable than matching on name.
- **Listings that appear in more than one account.** A listing can exist in two platform accounts
  simultaneously. If only one has activity in a period there is no double-count, but check both
  every period rather than assuming.
- **Listings with no PMS mapping.** Any channel listing that does not map to a PMS property is a
  future revenue leak. Resolve it before it books.

## Update rules

- Record only labels and property/listing mappings.
- Do not store login email unless operationally necessary and explicitly wanted.
- Never store passwords, MFA, recovery data, payment accounts, or session cookies.
- If a property moves between platform accounts, date the change rather than overwriting history.
