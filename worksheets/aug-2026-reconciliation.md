# VILANO101 — August 2026 tax reconciliation worksheet

**Source:** `ownerrez-bookings-2026-09-01.json` (pulled 2026-09-01, 16 properties, 2,770 bookings, `include_charges=true`)
**Basis shown:** arrival month = 2026-08. See period-basis warning below.
**Status:** DRAFT — not approved, not filed. Gate 1 not yet presented.

---

## 1. Marketplace posture — ESTABLISHED FROM EVIDENCE

Per-booking effective rates, 38 active August-arrival bookings. Not assumed — measured.

| Channel | n | Taxable base | FL state | Surtax | County bed tax |
|---|---:|---:|---|---|---|
| **Airbnb** | 22 | $42,676.00 | **0.000%** | **0.000%** | **5.000%** |
| **Vrbo** | 10 | $21,955.57 | 6.000% | 0.500% | 5.000% |
| **Direct / none** | 3 | $7,591.29 | 6.000% | 0.500% | 5.000% |
| **My Website** | 3 | $3,800.34 | 6.000% | 0.500% | 5.000% |

**Conclusion:**
- **Airbnb remits Florida state sales tax and the discretionary surtax. It does NOT remit
  St. Johns County TDT** — that passes through to the business on every one of the 22 bookings,
  at exactly 5.000%, with zero state tax lines.
- **Vrbo remits nothing.** All three taxes pass through to the business.
- Direct and website bookings: all three taxes are the business's responsibility.

This confirms the general expectation for St. Johns County, but it is now established from
this account's own August data rather than from a secondary source.

---

## 2. Taxable base and expected tax

### DR-15 (Florida Department of Revenue)

| Line | Amount |
|---|---:|
| Gross rental receipts, all channels | $76,023.20 |
| Less marketplace-facilitator sales (Airbnb) | ($42,676.00) |
| **Host-remitted taxable base** | **$33,347.20** |
| Expected state tax @ 6.0% | $2,000.83 |
| Expected discretionary surtax @ 0.5% | $166.74 |
| **Expected DR-15 tax** | **$2,167.57** |
| Actually collected in OwnerRez | $2,130.54 |
| **Under-collected** | **($37.03)** |

> Airbnb sales are still **reported** as gross sales on the DR-15 and then deducted as
> marketplace sales. They are not simply omitted.

### St. Johns County Tourist Development Tax

| Line | Amount |
|---|---:|
| Taxable base — **all channels, Airbnb included** | $76,023.20 |
| Expected TDT @ 5.0% | $3,801.16 |
| Actually collected in OwnerRez | $3,772.67 |
| **Under-collected** | **($28.49)** |
| Collection allowance (2.5% of first $1,200, cap $30) | ($30.00) |
| **Expected payment** | **$3,771.16** |

**Total under-collection across both returns: $65.52.**

---

## 3. The two bookings causing the under-collection

Every other booking computed at exactly 6.000% / 0.500% / 5.000%. These two did not:

| Booking | Property | Channel | Taxable base | Base actually taxed | Gap |
|---|---|---|---:|---:|---:|
| 17962851 | Pink Flamingo | direct | $2,951.14 | $2,711.17 | $239.97 |
| 18749203 | Coco | Vrbo | $849.84 | $519.83 | $330.01 |

Effective rates were 5.51%/4.59%/0.46% and 3.67%/3.06%/0.31% respectively.

Consistent with charges added **after** tax was computed. This is the known PMS failure mode:
a taxable-charges column can exceed the base the system actually taxed.

**Treatment per operating rules:** file on the **verified base** ($76,023.20 / $33,347.20),
not on tax collected. Log the $65.52 under-collection separately. **Do not change OwnerRez tax
settings during the filing run** — raise a separate authorised audit afterwards.

---

## 4. Cancelled bookings with retained charges — RESOLVED: ALL FORFEITURES

**Owner confirmed 2026-09-09 that all three retentions were forfeitures**, and therefore
taxable. Recorded in `decisions.json`.

> **The figures in sections 2 and 3 below EXCLUDE these** — they were computed before the
> determination. The period totals as filed:
>
> | | Sections 2–3 below | **As filed** |
> |---|---:|---:|
> | TDT base (all channels) | $76,023.20 | **$77,647.63** |
> | DR-15 base (host-remitted) | $33,347.20 | **$34,971.63** |
> | DR-15 tax @ 6.5% | $2,167.57 | **$2,273.16** |
> | TDT tax @ 5.0% | $3,801.16 | **$3,882.38** |
>
> All three are Vrbo bookings, so the business remits every tax on them.
>
> **August returns filed, and the tax on these forfeitures was paid** (owner confirmed
> 2026-09-09). Period closed. Use the "as filed" column.

Retained, unrefunded charges on a cancelled booking are a taxable event where the
guest had a guaranteed right to occupy.

| Booking | Property | Paid | Refunded | Retained | Base | Tax |
|---|---|---:|---:|---:|---:|---:|
| **17213461** | Pink Flamingo | $1,657.79 | $0.01 | **$1,657.78** | $1,486.80 | $170.98 |
| 17492584 | Pink Flamingo | $1,430.40 | $1,341.23 | $89.17 | $79.97 | $9.20 |
| 17393281 | The Palms | $1,071.51 | $1,007.22 | $64.29 | $57.66 | $6.63 |

The first is material. If those retentions were forfeitures rather than released deposits,
they add **$1,624.43** of taxable base and belong on both returns.

Eight further August-arrival cancellations had $0 paid and $0 retained — no tax consequence.

---

## 5. Property roster — 11 active, 5 snoozed (operator-confirmed 2026-09-01)

16 OwnerRez properties. The split is exact and maps perfectly onto August activity:
every active property had August arrivals; no snoozed property did.

**11 ACTIVE — all in this return:** Pink Flamingo · SeaBreeze · Coco · Pearl · Sunny ·
Vilano Bliss · Olive · The Palms · Family Tides · Coastal Duo · Pink Palms Retreat

**5 SNOOZED — none in this return:**

| Property | Active bookings | Last arrival | Future arrivals | Situation |
|---|---:|---|---:|---|
| **Ruby** (605 Twentieth) | 86 | 2027-03-16 | **4** | Snoozed but **still has forward bookings** — will owe tax in a future period. The Brendon Horn / VILANO PROPERTIES LLC entity question is deferred, not resolved. |
| **True Blue** (3877 Laurel) | 322 | **2026-07-22** | 0 | **Had July 2026 revenue.** Belongs on a July return if July is unfiled. |
| June-up | 0 | never | 0 | New (id 495095), zero booking rows of any kind |
| Vida | 0 | never | 0 | New (id 495097), zero booking rows |
| Viv-down | 0 | never | 0 | New (id 495096), zero booking rows |

The August return is unaffected by the snoozed set. **July is not** — True Blue was still
transacting through 22 July 2026.

---

## 6. Combo listings — no double-count

Both combo listings and their component homes appear, but each booking is a distinct stay on a
distinct listing, and a combo is unbookable whenever a component sells. Summing all listings is
correct here and does **not** double-count.

August active arrivals by listing: Coastal Duo 1 · Coco 5 · Family Tides 2 · Olive 3 ·
Pearl 5 · Pink Flamingo 5 · Pink Palms Retreat 1 · SeaBreeze 5 · Sunny 4 · The Palms 3 ·
Vilano Bliss 4 = 38.

---

## 7. ⚠ PERIOD BASIS — UNRESOLVED AND MATERIAL

The taxable base swings enormously with the basis chosen:

| Basis | Active bookings | Taxable base |
|---|---:|---:|
| **Arrival in August** | 38 | **$76,023.20** |
| Departure in August | 41 | $92,297.08 |
| Booked in August | 51 | $114,004.65 |

A $37,981 spread between arrival and booked basis. Everything above uses **arrival**.

St. Johns County's own wording is *"due on the first of the month following **collection**"*,
which points at a collection (cash-receipts) basis — matching neither figure exactly. A true
collection-basis figure needs payment-level data, which this snapshot does not carry.

**This must match the basis used in prior Vilano101 filings.** Confirm before submitting.
Do not switch bases between periods.

---

## 8. Open items before Gate 1

1. **Period basis** — arrival, departure, or collection. Blocking.
2. **Cancellation forfeitures** — are the three retained amounts forfeitures? Adds $1,624.43 if so.
3. **Account numbers** — FL DOR certificate and St. Johns TDT account still not recorded.
4. **Consolidated vs per-location** — one DR-15 and one TDT return, or one per property.
5. **Prior-period consistency** — was July 2026 filed, and on what basis?
6. **Pearl micro-bookings** — three Airbnb bookings at $25/$25/$50 base, plus one $0 website
   booking. Legitimate but unusual; confirm they are real stays.
