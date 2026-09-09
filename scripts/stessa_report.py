"""Monthly Stessa entry report for VILANO101.

Reads the OwnerRez booking snapshot produced by the revenue project's
scripts/pull_bookings.py and writes a human-readable report that a staff member
keys into Stessa BY HAND. Nothing here touches Stessa. That is deliberate.

Accounting basis, decided by the owner 2026-09-09:
  - GROSS    : income is what the guest was charged; platform fees are an expense
  - ACCRUAL  : a booking belongs to the month of ARRIVAL (matches the tax returns)
  - TAX      : tax collected is recorded as income; tax remitted is an expense

Usage:
  python scripts/stessa_report.py 2026-08
  python scripts/stessa_report.py 2026-08 --snapshot "D:/path/to/ownerrez-bookings-YYYY-MM-DD.json"

Stdlib only. No dependencies.
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys
from collections import defaultdict

# ---------------------------------------------------------------------------
# RATES. Keep in sync with skill/resources/account-registry.yaml and re-verify
# every period. The report prints these so a mismatch is visible, not silent.
# ---------------------------------------------------------------------------
RATES = {
    "period_verified_for": "2026-08",
    "fl_state": 0.060,
    "st_johns_surtax": 0.005,
    "st_johns_tdt": 0.050,
}

# Channels where the MARKETPLACE remits Florida state tax + surtax. Established
# from booking evidence: these bookings carry no state tax line in OwnerRez.
# Re-establish from evidence every period; do not extend this set by assumption.
MARKETPLACE_REMITS_STATE = {"Airbnb"}

# OwnerRez listing -> street address. Update when a property is added.
ADDRESS = {
    "The Palms": "101 Meadow Ave",
    "Pink Flamingo": "109 Meadow Ave",
    "Sunny": "205 Fifth St",
    "Coco": "209 Eleventh St",
    "SeaBreeze": "211 Eleventh St",          # inferred - confirm
    "Pearl": "217 Eleventh St",
    "Olive": "505A Twentieth St",
    "Vilano Bliss": "507 Twentieth St",
    "Ruby": "605 Twentieth St",
    "True Blue": "3877 Laurel St",
}

# Combo listings: one OwnerRez listing covering two homes. Revenue is split to the
# physical homes by BEDROOM RATIO. This is a default, not a rule - the owner may
# prefer a different split. Change the weights here if so.
COMBOS = {
    "Family Tides":               {"Coco": 2, "SeaBreeze": 4},
    "Pink Palms Retreat":         {"Pink Flamingo": 4, "The Palms": 4},
    "Coastal Duo: Bliss & Olive": {"Olive": 2, "Vilano Bliss": 5},
}

DEFAULT_SNAPSHOT_GLOB = r"D:\Vilano 101\FreeWyld\freewyld\analysis\snapshots\ownerrez-bookings-*.json"

# Income buckets keyed by OwnerRez charge category. Order controls report order.
INCOME_BUCKETS = [
    ("rent",           "Rental income (incl. channel fee recovery)"),
    ("cleaning",       "Cleaning fees"),
    ("pet",            "Pet fees"),
    ("administrative", "Administrative fees"),
    ("booking",        "Credit card processing recovered"),
    ("_other",         "Other guest charges"),
    ("_tax",           "Taxes collected from guests"),
]


def money(x):
    if abs(x) < 0.005:
        return "$0.00"
    return f"${x:,.2f}" if x > 0 else f"-${-x:,.2f}"


def latest_snapshot():
    files = sorted(glob.glob(DEFAULT_SNAPSHOT_GLOB))
    if not files:
        sys.exit(f"No snapshot found at {DEFAULT_SNAPSHOT_GLOB}. Run the revenue "
                 f"project's scripts/pull_bookings.py first.")
    return files[-1]


def real_booking(b):
    return b.get("type") == "booking" and not b.get("is_block")


def split_charges(b):
    """Return (income_by_bucket, taxable_base, tax_by_description)."""
    inc = defaultdict(float)
    base = 0.0
    taxes = defaultdict(float)
    for c in b.get("charges") or []:
        amt = c.get("amount") or 0.0
        cat = c.get("category")
        typ = c.get("type")
        if cat == "tax" or typ in ("tax", "tax_other"):
            inc["_tax"] += amt
            taxes[c.get("description") or "(untitled tax)"] += amt
            continue
        key = cat if cat in {k for k, _ in INCOME_BUCKETS} else "_other"
        inc[key] += amt
        if c.get("is_taxable"):
            base += amt
    return inc, base, dict(taxes)


def blank_row():
    return {
        "n": 0,
        "combo_stays": 0,
        "income": defaultdict(float),
        "base_all": 0.0,        # taxable base, all channels -> TDT
        "base_host": 0.0,       # taxable base, host-remitted channels -> DR-15
        "host_fees": 0.0,
        "total_amount": 0.0,
        "bookings": [],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("period", help="YYYY-MM, e.g. 2026-08")
    ap.add_argument("--snapshot", help="path to ownerrez-bookings-*.json")
    ap.add_argument("--out", help="output .md path")
    a = ap.parse_args()

    period = a.period
    try:
        dt.datetime.strptime(period, "%Y-%m")
    except ValueError:
        sys.exit("period must be YYYY-MM")

    snap = a.snapshot or latest_snapshot()
    data = json.load(open(snap, encoding="utf-8"))
    acct = next(iter(data))
    bookings = data[acct]["bookings"]

    # Human decisions for this period (forfeiture calls on cancelled bookings).
    dec_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "decisions.json")
    decisions = {}
    if os.path.exists(dec_path):
        decisions = json.load(open(dec_path, encoding="utf-8")).get(period, {})
    forfeit_ids = set(decisions.get("forfeitures", []))

    sel = [b for b in bookings if real_booking(b) and str(b.get("arrival") or "")[:7] == period]
    canceled = [b for b in sel if b.get("status") == "canceled"]

    # A confirmed forfeiture is income and is taxable, so it joins the active set.
    # OwnerRez reduces a cancelled booking's charge lines to the retained amount, so
    # the charges are used as-is. Anything not decided stays out.
    forfeited = [b for b in canceled if b.get("id") in forfeit_ids]
    undecided = [b for b in canceled
                 if b.get("id") not in forfeit_ids
                 and (b.get("total_paid") or 0.0) - (b.get("total_refunded") or 0.0) > 0.005]
    active = [b for b in sel if b.get("status") == "active"] + forfeited

    # -------- per listing --------
    by = defaultdict(blank_row)
    for b in active:
        name = (b.get("property") or {}).get("name") or str(b.get("property_id"))
        inc, base, taxes = split_charges(b)
        r = by[name]
        r["n"] += 1
        for k, v in inc.items():
            r["income"][k] += v
        r["base_all"] += base
        if (b.get("listing_site") or "") not in MARKETPLACE_REMITS_STATE:
            r["base_host"] += base
        r["host_fees"] += b.get("total_host_fees") or 0.0
        r["total_amount"] += b.get("total_amount") or 0.0
        r["bookings"].append((b, inc, base, taxes))

    state_rate = RATES["fl_state"] + RATES["st_johns_surtax"]
    tdt_rate = RATES["st_johns_tdt"]

    def expenses(r):
        return {
            "host_fees": r["host_fees"],
            "dr15": r["base_host"] * state_rate,
            "tdt": r["base_all"] * tdt_rate,
        }

    # -------- allocate combos to physical homes --------
    homes = defaultdict(blank_row)
    for name, r in by.items():
        if name in COMBOS:
            w = COMBOS[name]
            tot = sum(w.values())
            for home, share in w.items():
                f = share / tot
                h = homes[home]
                h["combo_stays"] += r["n"]
                for k, v in r["income"].items():
                    h["income"][k] += v * f
                h["base_all"] += r["base_all"] * f
                h["base_host"] += r["base_host"] * f
                h["host_fees"] += r["host_fees"] * f
                h["total_amount"] += r["total_amount"] * f
        else:
            h = homes[name]
            h["n"] += r["n"]
            for k, v in r["income"].items():
                h["income"][k] += v
            h["base_all"] += r["base_all"]
            h["base_host"] += r["base_host"]
            h["host_fees"] += r["host_fees"]
            h["total_amount"] += r["total_amount"]

    # -------- write --------
    out = a.out or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                "worksheets", "stessa", f"{period}-stessa-entry.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    L = []
    w = L.append

    w(f"# VILANO101 — Stessa entry report — {period}")
    w("")
    w(f"Generated {dt.date.today().isoformat()} from `{os.path.basename(snap)}`.")
    w("")
    w("**For manual entry into Stessa by a staff member. Nothing in this report has been "
      "entered anywhere.** Stessa is not connected to any automation.")
    w("")
    w("| Basis | |")
    w("|---|---|")
    w("| Revenue | **Gross** — what the guest was charged. Platform fees are an expense. |")
    w("| Timing | **Accrual** — a booking belongs to its **arrival** month. Matches the tax returns. |")
    w("| Taxes | Tax **collected** is income. Tax **remitted** is an expense. |")
    w(f"| Rates | State {RATES['fl_state']:.1%} + surtax {RATES['st_johns_surtax']:.1%} = "
      f"{state_rate:.1%} on the DR-15 · County TDT {tdt_rate:.1%}. Verified for "
      f"{RATES['period_verified_for']} — **re-verify if filing a different period.** |")
    w(f"| Marketplace | {', '.join(sorted(MARKETPLACE_REMITS_STATE))} remits state + surtax; "
      f"the business remits county TDT on every channel. |")
    w("")

    # ---- Section 1: entry table by physical home ----
    w("## 1. Enter these — by physical home")
    w("")
    w("Combo listings are already split to their component homes by bedroom ratio "
      "(see section 3). One row per line item per home.")
    w("")
    tot = blank_row()
    for home in sorted(homes):
        h = homes[home]
        e = expenses(h)
        inc_total = sum(h["income"].values())
        exp_total = sum(e.values())
        addr = ADDRESS.get(home, "**address not on file — add to ADDRESS map**")
        w(f"### {home} — {addr}")
        w("")
        stays = f"Stays: {int(h['n'])}"
        if h["combo_stays"]:
            stays += f" · plus a share of {int(h['combo_stays'])} combo stay(s)"
        w(stays)
        w("")
        w("| Line | Amount | Type |")
        w("|---|---:|---|")
        for key, label in INCOME_BUCKETS:
            v = h["income"].get(key, 0.0)
            if abs(v) >= 0.005:
                w(f"| {label} | {money(v)} | income |")
        w(f"| **Total income** | **{money(inc_total)}** | |")
        w(f"| Platform host fees (Airbnb / Vrbo) | {money(-e['host_fees'])} | expense |")
        w(f"| FL sales tax + surtax remitted — accrued | {money(-e['dr15'])} | expense |")
        w(f"| St. Johns County TDT remitted — accrued | {money(-e['tdt'])} | expense |")
        w(f"| **Total expenses** | **{money(-exp_total)}** | |")
        w(f"| **Net** | **{money(inc_total - exp_total)}** | |")
        w("")
        tot["n"] += h["n"]
        for k, v in h["income"].items():
            tot["income"][k] += v
        tot["base_all"] += h["base_all"]
        tot["base_host"] += h["base_host"]
        tot["host_fees"] += h["host_fees"]
        tot["total_amount"] += h["total_amount"]

    # ---- Section 2: portfolio tie-out ----
    e = expenses(tot)
    inc_total = sum(tot["income"].values())
    w("## 2. Portfolio totals and tie-out to the tax returns")
    w("")
    w("| | Amount |")
    w("|---|---:|")
    for key, label in INCOME_BUCKETS:
        v = tot["income"].get(key, 0.0)
        if abs(v) >= 0.005:
            w(f"| {label} | {money(v)} |")
    w(f"| **Total income** | **{money(inc_total)}** |")
    w(f"| Check: sum of OwnerRez `total_amount` | {money(tot['total_amount'])} |")
    w(f"| Platform host fees | {money(-e['host_fees'])} |")
    w(f"| FL DR-15 remitted — accrued | {money(-e['dr15'])} |")
    w(f"| St. Johns TDT remitted — accrued | {money(-e['tdt'])} |")
    w(f"| **Net** | **{money(inc_total - sum(e.values()))}** |")
    w("")
    w("### Tax tie-out")
    w("")
    w("| | Base | Rate | Tax |")
    w("|---|---:|---:|---:|")
    w(f"| DR-15 — host-remitted channels only | {money(tot['base_host'])} | {state_rate:.1%} | {money(e['dr15'])} |")
    w(f"| St. Johns TDT — all channels | {money(tot['base_all'])} | {tdt_rate:.1%} | {money(e['tdt'])} |")
    w(f"| **Tax accrued as expense** | | | **{money(e['dr15'] + e['tdt'])}** |")
    w(f"| Tax collected from guests (income) | | | {money(tot['income'].get('_tax', 0.0))} |")
    diff = tot["income"].get("_tax", 0.0) - (e["dr15"] + e["tdt"])
    w(f"| **Collected minus remitted** | | | **{money(diff)}** |")
    w("")
    w("The accrued amounts are what the returns **should** show. When the returns are filed, "
      "confirm the filed figures match; if they differ, the filed figure wins and this report "
      "should be regenerated with a note. Collection allowances (up to $30 per return) are a "
      "portfolio-level credit — take them from the filed return, not from here.")
    w("")

    # ---- Section 3: combo split ----
    w("## 3. Combo listings — how they were split")
    w("")
    w("| Combo listing | Stays | Total income | Split to |")
    w("|---|---:|---:|---|")
    for name in sorted(COMBOS):
        if name in by:
            r = by[name]
            wts = COMBOS[name]
            t = sum(wts.values())
            parts = ", ".join(f"{h} {s}/{t}" for h, s in wts.items())
            w(f"| {name} | {r['n']} | {money(sum(r['income'].values()))} | {parts} |")
    w("")
    w("Split is by bedroom ratio. If the owner prefers a different split, change `COMBOS` in "
      "`scripts/stessa_report.py` and regenerate.")
    w("")

    # ---- Section 4: canceled with retained charges ----
    w("## 4. Cancelled bookings with retained charges")
    w("")
    if forfeited:
        note = decisions.get("note", "")
        who = decisions.get("decided_by", "owner")
        when = decisions.get("decided_on", "")
        w(f"**Confirmed as forfeitures by {who}{' on ' + when if when else ''} — these ARE "
          f"included as income in sections 1 and 2 above**, under the property shown. A "
          f"forfeited charge is taxable: the guest held a guaranteed right to occupy.")
        w("")
        w("| Booking | Property | Channel | Retained | Taxable base | Tax |")
        w("|---|---|---|---:|---:|---:|")
        ftb = ftx = fret = 0.0
        for b in sorted(forfeited, key=lambda x: -((x.get("total_paid") or 0) - (x.get("total_refunded") or 0))):
            inc, base, taxes = split_charges(b)
            ret = (b.get("total_paid") or 0.0) - (b.get("total_refunded") or 0.0)
            tx = sum(taxes.values())
            w(f"| {b.get('id')} | {(b.get('property') or {}).get('name','?')} | "
              f"{b.get('listing_site') or 'direct'} | {money(ret)} | {money(base)} | {money(tx)} |")
            ftb += base; ftx += tx; fret += ret
        w(f"| **Total** | | | **{money(fret)}** | **{money(ftb)}** | **{money(ftx)}** |")
        w("")
        if note:
            w(f"> {note}")
            w("")
        w(f"**Tax check:** these add {money(ftb)} of taxable base to the period. If the filed "
          f"returns did not include them, the period was under-reported by roughly "
          f"{money(ftb * state_rate)} on the DR-15 and {money(ftb * tdt_rate)} on the county "
          f"TDT. Confirm against the filed returns; correct by amendment or on the next "
          f"return as your CPA advises.")
        w("")
    if undecided:
        w("**Undecided — NOT included as income.** Decide each, then add the booking id to "
          "`decisions.json` under this period and regenerate.")
        w("")
        w("| Booking | Property | Channel | Retained | Decision |")
        w("|---|---|---|---:|---|")
        for b in undecided:
            ret = (b.get("total_paid") or 0.0) - (b.get("total_refunded") or 0.0)
            w(f"| {b.get('id')} | {(b.get('property') or {}).get('name','?')} | "
              f"{b.get('listing_site') or 'direct'} | {money(ret)} | ☐ forfeiture · ☐ released |")
        w("")
    if not forfeited and not undecided:
        w("No cancelled bookings retained money this period.")
        w("")

    # ---- Section 5: booking-level appendix ----
    w("## 5. Booking-level detail (audit trail)")
    w("")
    w("| Property | Booking | Arrival | Channel | Guest charged | Taxable base | Tax collected | Host fees |")
    w("|---|---|---|---|---:|---:|---:|---:|")
    for name in sorted(by):
        for b, inc, base, taxes in sorted(by[name]["bookings"], key=lambda x: x[0].get("arrival") or ""):
            w(f"| {name} | {b.get('id')} | {str(b.get('arrival'))[:10]} | "
              f"{b.get('listing_site') or 'direct'} | {money(b.get('total_amount') or 0)} | "
              f"{money(base)} | {money(sum(taxes.values()))} | {money(b.get('total_host_fees') or 0)} |")
    w("")
    w(f"{len(active)} active bookings · {len(canceled)} cancelled · arrival month {period}.")
    w("")

    open(out, "w", encoding="utf-8").write("\n".join(L))
    print(f"wrote {out}")
    print(f"  {len(active)} active bookings, {len(homes)} homes, income {money(inc_total)}, "
          f"net {money(inc_total - sum(e.values()))}")


if __name__ == "__main__":
    main()
