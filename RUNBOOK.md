# Monthly Tax Filing Runbook — VILANO101

For the person running the filing each month. Assumes no prior knowledge of this portfolio.

**Two returns, every month:**

| Return | Agency | Portal |
|---|---|---|
| **DR-15** Sales and Use Tax | Florida Department of Revenue | floridarevenue.com |
| **Tourist Development Tax** | St. Johns County Tax Collector | stjohnstax.us |

They are separate agencies with separate accounts, separate portals and separate payments.
Filing one does **not** file the other.

---

## Deadlines — read this before anything else

For a period ending the last day of month *M*:

| Milestone | When |
|---|---|
| Return due | 1st of month M+1 |
| **Electronic payment must be initiated** | **5:00 p.m. ET on the business day before the 20th** |
| Statutory delinquency | after the 20th (next business day if the 20th is a weekend or holiday) |

**The electronic payment deadline is earlier than the filing deadline, and they move in
opposite directions.** If the 20th falls on a weekend, the *return* deadline moves forward to
the next business day while the *payment* deadline moves backward to the previous business
day. Work to the payment date.

Confirm the exact payment date each period against **Form DR-659** (Florida eServices Calendar
of Electronic Payment Deadlines) for the current calendar year — the Sales and Use row.

**Worked example, August 2026 period:** due Tue 1 Sept · electronic payment by 5 p.m. ET Fri
18 Sept · statutory limit Mon 21 Sept. The operative deadline was the 18th.

Late costs: state 10% minimum $50 plus interest; county 10% per 30 days to a 50% maximum,
minimum $50, plus interest. The collection allowance is forfeited on both.

---

## Step 1 — Confirm the period is open and nothing prior is outstanding

1. Log in to both portals.
2. Confirm the period you intend to file is open, and check the assigned filing frequency on
   the account screen — the portal is authoritative, not this runbook.
3. Check that the **previous** period shows filed and paid. A period showing "processed" on a
   dashboard can still carry a pending amendment visible only when the return itself is opened.

A payment marked "in process" or "scheduled" is accepted, **not cleared**. Track those
separately and confirm the debit lands.

## Step 2 — Re-verify rates for the period being filed

Never carry a rate forward without checking. Rates can change mid-year.

| What | Where | Trap |
|---|---|---|
| State sales tax | GT-800034 | Stable at 6.0% |
| Discretionary surtax | **DR-15DSS for the correct calendar year** | The "current" URL `dr15dss.pdf` serves the **prior year**. The current-year file is `dr15dss_<yy>.pdf`. Check the printed calendar year. |
| County TDT | sjctax.us | **The county is authoritative over the state's summary table.** |

The $5,000 surtax cap does **not** apply to transient accommodations — surtax is due on the
full rental charge.

## Step 3 — Pull the booking data

From the revenue project (`vilano101-revenue-agent`):

```bash
python scripts/pull_bookings.py
```

This writes a dated snapshot to `analysis/snapshots/`. It must include charges — without charge
lines you cannot separate rent from fees from tax.

**The snapshot contains guest personal data. Never commit it to this repository.**

## Step 4 — Build the taxable base

Filter to real revenue bookings:

- `type == "booking"` — exclude `block`, `linked_availability`, `quote_hold`
- `is_block == False`
- Handle `status == "canceled"` separately (see step 5)

For each booking, split the charge lines:

- **Taxable base** — charges where `is_taxable` is true. This includes **cleaning fees** and
  required host fees, not just rent.
- **Tax lines** — `category == "tax"`. These are what was *collected*, which is not the same
  as what is *owed*.

### Two things that will bite you

**Combo listings.** Three listings cover two homes each — Family Tides (Coco + SeaBreeze),
Pink Palms Retreat (Pink Flamingo + The Palms), Coastal Duo (Olive + Vilano Bliss). Each combo
booking is a distinct stay, so summing all listings is correct and does not double-count. But
never treat a combo as a separate *property* for registration purposes — it has no address.

**Snoozed properties still owe tax for periods they were active in.** Current listing status
does not determine period scope. A house snoozed today may have had stays in the period being
filed. Scope from the booking data, not from what is live now.

## Step 5 — Check cancellations for retained charges

A cancelled booking with a **retained, unrefunded** charge is generally a taxable event where
the guest had a guaranteed right to occupy — even though nobody stayed.

Test: `total_paid > 0` and `total_refunded < total_paid` and `status == canceled`.

A *released* security deposit is not part of the base. Only *retained* charges are.
Marketplaces often tax these correctly while the PMS does not flag them.

## Step 6 — Split by channel and confirm marketplace posture

Group the base by `listing_site` and compute each channel's effective tax rate
(tax collected ÷ taxable base).

**Ratio test:** a channel showing ~5.0% county tax and 0.0% state tax means the marketplace
remitted the state portion and passed the county through. A channel showing 6.0% / 0.5% / 5.0%
means everything falls to the business.

**Establish this every period from that period's evidence.** Platforms change posture, and two
platforms in the same county can behave in opposite ways.

## Step 7 — Reconcile expected against collected

Compute expected tax at the verified rates and compare with what OwnerRez actually collected.

Where they differ:

- **File on the verified base**, not on tax collected.
- Log the over- or under-collection separately.
- **Do not change OwnerRez tax settings during the filing run.** Open a separate authorised
  audit afterwards.

A PMS taxable-charges column can exceed the base it actually taxed. Reconcile the two rather
than assuming the tax figure implies the base.

Classify every variance: explained and documented · open and unexplained · material ·
immaterial · needs government or CPA verification. Do not round a difference away.

## Step 8 — GATE 1: approve the filing packet

Produce a packet per return using `skill/templates/pre-filing-packet.md`, showing period,
jurisdiction, entity, account, properties, gross receipts, taxable base, marketplace-remitted
base by channel, business-remitted base, rates with effective dates, tax before allowance,
allowance, expected payment, variances, and unresolved issues.

**A human approves this before any figure is entered into a portal.**

## Step 9 — File

### DR-15 (Florida DOR)

Report **gross rental receipts for all channels**, then deduct marketplace-facilitator sales
(Airbnb) as exempt. Airbnb revenue is reported and deducted — not omitted.

Rent goes on Line D; surtax on Line 15(d). Let the portal compute the collection allowance.

### St. Johns County TDT

The county 5% is owed on **all channels including Airbnb**. Airbnb does not remit it.

## Step 10 — GATE 2: approve the irreversible action

At the final review screen, confirm what the portal itself shows: account, period, base, tax,
allowance, penalty, fee, total debit, debit date, masked payment method.

**Do not click submit, file, pay or authorize until a human approves the figures on screen.**
If filing and payment are separate irreversible actions, approve each.

If the portal total differs from your packet, **stop before submitting** and explain the gap.

### If the portal errors mid-transaction

**Verify the return's status before re-filing.** Never resubmit blind on a live tax account. A
well-behaved portal rolls back cleanly — confirm it, don't assume it.

Prefer **ACH** over card. Convenience fees vary by method and card can cost substantially more
for identical settlement. Card and e-check payments are often non-cancellable once made.

## Step 11 — Close the period

1. Save the filing confirmation and the payment receipt.
2. Record the confirmation number and whether payment is **scheduled** or **cleared**.
3. Save the source export and the reconciliation worksheet.
4. Complete `skill/templates/close-summary.md`.
5. Carry unresolved issues forward.

**Keep confirmations and receipts out of this public repository** — `.gitignore` blocks
`confirmations/`, `receipts/` and `filed/`.

A period is closed only when every account reads one of: filed and paid or scheduled with
confirmation · zero return filed and confirmed · not due and documented · blocked with owner
and next action.

A zero-tax period usually still requires a return. "Not due" and "unfiled" are different
states — document which applies and why.

---

## Open items to resolve before the next filing

1. **Period basis.** Arrival, departure or collection basis changes the taxable base
   enormously — for August 2026 the spread was $76,023 / $92,297 / $114,005. The county's
   wording points at a collection basis. **Whatever prior periods used, keep using.** Do not
   switch bases between periods.
2. **Consolidated or per-location registration.** One DR-15 and one TDT return covering all
   properties, or one of each per rental address. The county's TDT application is
   one-address-per-form, which leans per-location.
3. **Account numbers.** Both are `PENDING_USER_ENTRY` in the registry. Obtain from the DR-11
   certificate and the county portal. Enter with confidence `VERIFIED_DOCUMENT` or
   `VERIFIED_LIVE_PORTAL` — never from a historical note.
4. **605 Twentieth St (Ruby).** Snoozed but holds forward bookings. Deed-verified to a
   different owner, and its DBPR licence is held by a different entity. Resolve before its
   revenue lands on a VILANO101 return.
5. **Was July 2026 filed?** True Blue was still transacting through 22 July 2026.

## Never

- Retype a government account number from memory when a registry value exists
- Merge two similar account numbers or "correct" a digit by intuition
- Assume Airbnb and Vrbo remit the same tax types
- Assume state tax and county tax are handled together
- Use tax collected as a substitute for a verified taxable base
- Change tax settings, account registrations or property mappings during a filing run
- Mark a period complete while any account is merely prepared or awaiting confirmation
