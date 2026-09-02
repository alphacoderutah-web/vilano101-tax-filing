# VILANO101 — Monthly Tax Filing

Florida sales and use tax (DR-15) and St. Johns County Tourist Development Tax for the
VILANO101, LLC short-term rental portfolio in St. Augustine, Florida.

This repository holds the filing procedure, the verified account registry, the rate and
deadline reference, and worked reconciliation worksheets. One person runs it once a month.

**Start here:** [`RUNBOOK.md`](RUNBOOK.md) — the monthly step-by-step.

---

## ⚠ THIS IS A PUBLIC REPOSITORY

Everything committed here is world-readable, and **git history is permanent** — deleting a
file in a later commit does not remove it from history, forks, or caches.

### Never commit these

| Never | Why |
|---|---|
| Passwords, MFA codes, PINs, recovery codes | Account takeover |
| API tokens (OwnerRez, PriceLabs) | Full read/write to live systems |
| FEIN or SSN | Identity theft |
| Bank routing / account numbers, card numbers | Direct financial loss |
| **OwnerRez booking exports** | They carry **guest email addresses, guest ids, reservation numbers and free-text notes** — your guests' personal data, not the business's |
| Filing confirmations and payment receipts | Contain submitted figures and payment references |

The [`.gitignore`](.gitignore) blocks the common shapes of these. It is a safety net, not a
substitute for looking before you commit.

### Already public in this repo

Committed deliberately by the account owner, who was advised of the exposure and chose to
proceed:

- Entity identity — VILANO101, LLC, Sunbiz L21000525709
- All property street addresses
- Owner names of record (also public via deed and Property Appraiser records)
- Licence and registration numbers — DBPR, business tax receipt, parcel and deed references
- Monthly revenue by property

**Government tax account numbers are NOT yet in this repo.** `account-registry.yaml` carries
`PENDING_USER_ENTRY` for both the Florida DOR certificate and the St. Johns County TDT
account. Adding them is the single largest step-change in exposure this repository can take —
those numbers plus the entity name are what a portal account-recovery flow asks for. Consider
keeping them out of the public repo and supplying them to the filer separately.

---

## What this portfolio is

| | |
|---|---|
| Filer of record | VILANO101, LLC (Sunbiz L21000525709) |
| Market | St. Augustine, FL — St. Johns County only |
| PMS | One OwnerRez account |
| Properties | 16 OwnerRez records — **11 active, 5 snoozed** |
| Physical homes, active | **8 addresses** (3 of the 11 active listings are combos) |
| Returns per month | Florida DR-15 + St. Johns County TDT |

### Rates (verified for August 2026 — re-verify every period)

| Component | Rate | Remitted to |
|---|---|---|
| Florida state sales tax | 6.0% | DOR, on the DR-15 |
| St. Johns discretionary surtax | 0.5% | DOR, on the DR-15 |
| St. Johns Tourist Development Tax | 5.0% | **County Tax Collector — separate return** |
| **Guest-facing total** | **11.5%** | |

### Marketplace posture (established from August 2026 booking evidence)

| Channel | State + surtax | County TDT |
|---|---|---|
| **Airbnb** | Airbnb remits | **Business remits** |
| Vrbo | Business remits | Business remits |
| Direct / website | Business remits | Business remits |

**Airbnb does not remit St. Johns County TDT.** This is the most common compliance failure in
this county. Re-establish it from evidence every period rather than trusting this table.

---

## Layout

```
README.md                     this file
RUNBOOK.md                    monthly step-by-step
skill/
  SKILL.md                    filing procedure, controls, approval gates
  resources/
    account-registry.yaml     entity, properties, accounts, rates, deadlines
    operating-rules.md         non-negotiable filing controls
    portal-workflows.md        portal navigation
    platform-data-protocol.md  how to pull and treat source data
    official-source-checks.md  what to re-verify each period
    learning-log.md            durable lessons from real filing cycles
    verified-tax-accounts.md   government document summaries
    property-account-map.md    property to account mapping logic
    platform-account-map.md    platform account mapping
  templates/
    pre-filing-packet.md       Gate 1 approval packet
    close-summary.md           period close record
worksheets/
  aug-2026-reconciliation.md   worked example — August 2026
```

## Two rules that matter more than the rest

1. **Nothing irreversible without human approval.** The procedure has two gates: approve the
   filing packet before figures are entered, and approve the final screen before any submit,
   file, pay or authorize action. Both are human decisions.
2. **Never change tax settings during a filing run.** If collected tax disagrees with expected
   tax, file on the verified base, log the variance, and open a separate audit afterwards.
