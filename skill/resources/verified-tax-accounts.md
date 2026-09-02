# Verified Tax Accounts and Government Instructions

**Template.** This file is where the non-secret operational facts from your government tax
documents get summarised. It ships empty so the skill can be published; populate it locally and
keep the populated copy private.

## Source authority

Facts labelled `VERIFIED_DOCUMENT` come from printed government registration or notice
documents. Facts labelled `VERIFIED_LIVE_PORTAL` were read off an authenticated portal account
screen. Handwritten annotations are preserved only when operationally useful and are labelled
historical, never as current rules.

## What to record per Florida DOR certificate

- Entity name exactly as registered
- Certificate number (format `NN-NNNNNNNNNN-N`)
- Registration effective date
- Which properties file under it
- Source of the value
- Any penalty-waiver history

**Penalty-waiver notices are a control input, not trivia.** A first-occurrence waiver typically
warns that future errors may incur a penalty of 10% of tax due or $50 (whichever is greater),
plus interest and loss of the collection allowance, and that future penalties may not be waived.
Any account with such history should be treated as a heightened deadline-control account and
completed at least 3 business days before the electronic deadline.

## What to record per county TDT account

County tourist-development-tax accounts are usually observed in the portal rather than issued on
a document, so they start at `HISTORICAL_PORTAL_OBSERVED` / `needs_live_verification: true`.

**Do not trust historical county account numbers.** In one real cycle all three county account
numbers held in a registry were wrong — the live portal showed 7-digit numbers where the registry
held 6-digit ones, and the differences were not a single consistent transformation. Read them off
the live portal every period before entering figures.

## What to record for Utah

- TAP customer account number
- Sales and Use Tax (STC) account, filed on TC-62M or TC-62S
- Sales Transient Room (STR) account, filed on TC-62T
- Filing frequency **as shown live in TAP** — historical operating memory is not authoritative

Utah account letters typically instruct the business to file a return for every filing period and
tax type even when no tax is due, to use the exact account number shown, and to check current
rates because they may change quarterly.

## Deliberately excluded

Never record in this or any other skill file:

- FEINs or SSNs
- PINs
- bank routing numbers
- bank account numbers
- card numbers
- portal passwords, MFA/recovery codes, or password-manager secrets
- login user IDs where not operationally required

Authentication and payment credentials belong in the browser or a password manager, entered by a
human, never in a repository.
