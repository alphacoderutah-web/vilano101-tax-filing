---
name: str-tax-filing
description: Reconcile, prepare, and execute Florida and Utah vacation-rental sales, tourist-development, and transient-room tax filings across multiple OwnerRez, Airbnb, and Vrbo accounts. Manual invocation only.
disable-model-invocation: true
argument-hint: "[period e.g. 2026-07 or 2026-Q3] [florida|utah|all] [dry-run]"
---

# STR Tax Filing

Operate as the tax-close controller for a multi-property vacation-rental business in Florida and Utah. This is a high-stakes filing/payment workflow. Accuracy, account selection, source traceability, reconciliation, deadline control, and human approval are mandatory.

## Load order

Before any filing work, read in this order:

1. `${CLAUDE_SKILL_DIR}/resources/account-registry.yaml`
2. `${CLAUDE_SKILL_DIR}/resources/verified-tax-accounts.md`
3. `${CLAUDE_SKILL_DIR}/resources/operating-rules.md`
4. `${CLAUDE_SKILL_DIR}/resources/property-account-map.md`
5. `${CLAUDE_SKILL_DIR}/resources/platform-account-map.md`
6. `${CLAUDE_SKILL_DIR}/resources/platform-data-protocol.md`
7. `${CLAUDE_SKILL_DIR}/resources/portal-workflows.md`
8. `${CLAUDE_SKILL_DIR}/resources/official-source-checks.md`
9. `${CLAUDE_SKILL_DIR}/resources/learning-log.md`
10. `${CLAUDE_SKILL_DIR}/templates/pre-filing-packet.md`
11. `${CLAUDE_SKILL_DIR}/templates/close-summary.md`

## Invocation

Interpret `$ARGUMENTS` as filing period, jurisdiction scope, and mode.

Examples:

- `/str-tax-filing 2026-07 florida`
- `/str-tax-filing 2026-07 florida dry-run`
- `/str-tax-filing 2026-Q3 utah`
- `/str-tax-filing 2026-Q3 all dry-run`

If the filing period is omitted, identify the most recent open period from current portal/account records. Do not guess.

`dry-run` means gather, calculate, reconcile, and prepare the full filing packet, but do not submit any return, initiate any payment, or make any portal/account changes.

## Filing universe

The business uses:

- 2 OwnerRez accounts
- 2 Airbnb accounts
- 2 Vrbo accounts
- Florida DOR Sales and Use Tax
- Flagler County Tourist Development Tax
- St. Johns County Tourist Development Tax
- Utah TAP Sales and Use Tax
- Utah TAP Sales Transient Room Tax

Florida is generally handled monthly in the current operating system. The known Utah St. George/Washington County group has historically been handled quarterly, but the live TAP account period/frequency is authoritative.

## Hard security boundary

Never store or write into skill files, notes, logs, generated worksheets, or prompts:

- passwords
- MFA or recovery codes
- PINs
- full FEIN/SSN values unless an official filing form absolutely requires transient use on-screen
- bank routing numbers
- bank account numbers
- full card numbers
- password-manager secrets
- login user IDs when not operationally required

The source packet used to build this skill contained credential-like and banking annotations. Those values were intentionally excluded from the skill.

The user should type passwords/MFA directly into the browser or approve a password manager. Claude resumes after authentication.

## Account-number authority rule

For tax account/certificate selection:

1. Current live government portal/account record
2. User-supplied government registration/notice documents summarized in `verified-tax-accounts.md`
3. Prior filed return/payment confirmation
4. Historical master-prompt notes

If a historical account number conflicts with a user-supplied government document, use the government document and log the correction. Never blend digits from two sources.

At least one certificate in this portfolio is a known corrected conflict where an older note transposed digits. Always use the verified registry value, never the historical one. Record such corrections explicitly in the registry so they cannot silently reappear.

## Non-negotiable controls

1. Reconcile before filing.
2. Never assume Airbnb and Vrbo remit the same tax types.
3. Never assume Florida state sales tax and county TDT are handled together.
4. Never use tax collected as a substitute for a verified taxable revenue base when charge mappings are suspect.
5. Never change OwnerRez tax settings during a filing run. Log issues for a separate authorized audit.
6. Never change tax-account registrations, property mappings, or entity ownership from a monthly filing workflow without explicit user authorization.
7. Verify current rates, due dates, marketplace treatment, and portal form behavior from official sources for every filing period.
8. Use the exact government account/certificate that maps to the property/entity being filed.
9. A zero-tax period still requires a return wherever the current portal/instructions require one.
10. Preserve filing and payment confirmations immediately after submission.
11. Do not mark a period complete while any in-scope account remains merely prepared, pending review, or missing confirmation evidence.
12. If a portal total differs from the pre-filing calculation, stop before submission and explain the variance.

## Approval gates

### Gate 1 - approve filing packet

Before entering final filing figures into a government return, show a consolidated pre-filing packet containing every account in scope:

- period
- jurisdiction and tax type
- entity
- government account/certificate
- properties included
- platform accounts/data sources included
- gross receipts
- taxable base
- marketplace-remitted/excluded base by channel and tax type
- business-remitted base
- rates used and effective dates
- tax before allowance
- allowance/discount
- penalty/interest
- expected government payment
- service fee if known
- variances and explanations
- confidence classification
- unresolved issues

Wait for explicit approval.

### Gate 2 - approve irreversible portal action

At the final live review screen, present exactly what the portal shows:

- portal
- account/certificate
- entity/property group
- period
- taxable base
- tax due
- allowance/discount
- penalty/interest
- service fee
- total debit/payment
- debit date
- masked payment method if visible

Do not click an irreversible **submit**, **file**, **pay**, **authorize**, or equivalent action until the user explicitly approves the presented figures.

If filing and payment are separate irreversible actions, obtain approval for each unless the user explicitly approves both after both amounts/actions are clearly listed.

## Workflow

### Phase 0 - deadline and prior-risk check

1. Resolve filing period and scope.
2. Determine each in-scope account's current filing frequency and due date from portal/official instructions.
3. Identify accounts with prior penalty/late-filing history in `verified-tax-accounts.md`.
4. Flag any filing within 3 business days of an electronic payment deadline as HIGH operational urgency.
5. If already late, calculate/verify portal penalty and interest; do not assume a waiver.

### Phase 1 - establish current account matrix

Build a run-specific matrix:

`property -> entity -> platform account -> county/state -> tax type -> government account -> filing frequency`

Use `account-registry.yaml` as the starting map and verify any `needs_live_verification: true` items before filing.

### Phase 2 - gather source data

Gather current-period records from both accounts of each applicable platform:

- OwnerRez 1
- OwnerRez 2
- Airbnb 1
- Airbnb 2
- Vrbo 1
- Vrbo 2

Use `platform-data-protocol.md`. Prefer downloaded reports/exports. Preserve originals unmodified.

### Phase 3 - normalize booking-level data

For each transaction:

1. Identify property.
2. Identify entity and government filing account.
3. Identify booking channel.
4. Determine the correct filing-period basis used for that tax/account.
5. Separate guest stays, owner stays, cancellations/refunds, and non-tax transactions.
6. Break charges into rent, cleaning, pet fees, damage protection/deposits, required host fees, optional charges, and taxes.
7. Determine which charges are taxable under current official rules.
8. Identify which tax types were remitted by marketplace versus collected/remitted by the business.

### Phase 4 - reconcile

Reconcile at booking, property, channel, tax-type, and filing-account level:

- OwnerRez taxable base
- Airbnb evidence
- Vrbo evidence
- direct/manual booking records
- tax collected by platform
- tax collected by business
- expected tax at verified rates
- portal-calculated tax

Classify every variance:

- EXPLAINED_DOCUMENTED
- OPEN_UNEXPLAINED
- MATERIAL_HIGH_RISK
- IMMATERIAL_NOTED
- NEEDS_GOVERNMENT_OR_CPA_VERIFICATION

### Phase 5 - prepare filing packets

Prepare one account packet per government return using `templates/pre-filing-packet.md`, plus a consolidated Gate 1 summary.

Obtain Gate 1 approval.

### Phase 6 - execute portal workflow

Follow `portal-workflows.md`.

The user handles authentication/MFA/CAPTCHA. Claude may navigate, select the correct verified tax account/certificate, enter non-secret filing figures, upload templates, calculate, and review.

At the final irreversible step, obtain Gate 2 approval.

### Phase 7 - archive and close

After each filing/payment:

1. Save filing confirmation/return.
2. Save payment confirmation/receipt.
3. Record confirmation/reference number.
4. Record payment status as `scheduled/in process` versus `cleared`.
5. Save current source exports and reconciliation worksheet.
6. Update the close summary.
7. Carry unresolved issues forward.
8. Update `learning-log.md` only for durable verified procedural facts or user-confirmed mappings.
9. Never copy secrets into the learning log.

## Completion standard

Every in-scope account must finish as one of:

- `FILED_PAID_OR_SCHEDULED_CONFIRMED`
- `ZERO_RETURN_FILED_CONFIRMED`
- `NOT_DUE_DOCUMENTED`
- `BLOCKED_WITH_OWNER_AND_NEXT_ACTION`

Only then may the period be called closed.
