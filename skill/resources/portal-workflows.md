# Portal Workflows

Use live labels as authoritative. Portal UI can change.

## Authentication protocol

For every portal:

1. Open the official login page.
2. Ask the user to take over for password/password-manager/MFA/CAPTCHA if needed.
3. Do not copy credentials into Claude notes or files.
4. Resume after the authenticated account screen is visible.
5. Verify the selected government account/certificate against `account-registry.yaml` before entering figures.

---

## St. Johns County Tourist Development Tax

Login/filer URL:

`https://www.stjohnstax.us/Account/Login?ReturnUrl=../TDTFiling.aspx`

Historical workflow observations:

- Multiple account/property rows may appear on one filing page.
- Business names can differ by row.
- Individual rows or a batch submission control may be available.
- Filings may be added to a payment cart.
- Service fee may appear; record tax and fee separately.
- Receipt may contain a Paystar/reference number.

Expected historical account rows, all requiring live verification:

- `<PROPERTY-01>`: `<COUNTY-TDT-ACCT-C>`
- `<PROPERTY-02>`: `<COUNTY-TDT-ACCT-D>`
- `<PROPERTY-03>`: `<COUNTY-TDT-ACCT-E>`

Controls:

- Verify the current 5% county rate from an official St. Johns source/portal before filing.
- Verify taxable-base instructions and marketplace treatment for the period.
- Confirm the live row maps to the expected property before submitting.
- Stop at Gate 2.

---

## Flagler County Tourist Development Tax - Tourist Express

Login URL:

`https://flagler.county-taxes.com/tourist/profile/log_in`

Historical account mapping, requiring live verification:

- `<ENTITY-A>` group: account `<COUNTY-TDT-ACCT-A>`
- `<ENTITY-B>` property: account `<COUNTY-TDT-ACCT-B>`

Current official Flagler guidance should be checked at:

`https://www.flaglertax.gov/tourist-development-tax/`

Known workflow:

- Tourist Express may use a supplemental property spreadsheet/template.
- Preserve the downloaded workbook structure exactly.
- Never invent a missing property row.
- If a property is missing from the template, stop the upload path and resolve the account/property-list issue.
- Save both filed return and receipt/confirmation.

Control points to re-verify every period:

- TDT is 5% of taxable rental receipts.
- Official page lists room rate, cleaning, pet fees, and traveler service fees as taxable; damage deposits and optional travel insurance as non-taxable examples.
- Current page says due on the 1st and delinquent after the 20th; a return is required even if no tax was collected.
- Online timely filing/payment may receive 2.5% of first $1,200 tax due, max $30.

Re-verify before every period. Stop at Gate 2.

---

## Florida Department of Revenue - Sales and Use Tax

Entry page supplied by user:

`https://floridarevenue.com/taxes/eservices/Pages/sutlogin.aspx`

Current exact Florida DOR certificates live in `account-registry.yaml`. Never retype one from
memory, and never "correct" a digit by intuition — read it from the registry and confirm it
against the authenticated portal screen before entering figures.

| Entity/property group | Certificate |
|---|---|
| `<ENTITY-A>` / `<GROUP-A>` | `<FL-DOR-CERT-A>` |
| `<ENTITY-B>` / `<GROUP-B>` | `<FL-DOR-CERT-B>` |

**Where a historical value has been superseded, record the deprecated number explicitly in the
registry so it cannot silently reappear.**

Workflow controls:

1. Authenticate via the current enrolled-user / filing path.
2. Select the exact certificate/account for the return.
3. Select the current reporting period.
4. Use the current DR-15 transient-rental entry path shown by the portal/instructions.
5. Gross/taxable rental sales should exclude tax collected.
6. Confirm current county discretionary surtax rate for the property's county.
7. The historical DR-15 workflow used the discretionary surtax allocation line as a reporting/allocation line, not a second tax charge. Follow current instructions and avoid double-counting.
8. Let portal-calculated collection allowance calculate when appropriate.
9. Compare portal amount to the Gate 1 packet.
10. If different, stop and reconcile.
11. Stop for Gate 2 before filing/payment.
12. Save confirmation immediately.
13. Record `In Process`/scheduled separately from cleared.

DOR timing control to re-verify every period:

- Current DR-15 instructions state returns/payments are due on the 1st and late after the 20th following the reporting period.
- Electronic payments must be initiated and receive a confirmation by the DOR-specified electronic cutoff (currently 5 p.m. ET on the business day before the 20th under current instructions).
- A return is required for each reporting period even if no tax is due.

Always re-check current DR-15 instructions/calendar.

---

## Utah Taxpayer Access Point (TAP)

Portal:

`https://tap.utah.gov/`

Account identifiers live in `account-registry.yaml`:

- Customer: `<UT-CUSTOMER>`
- Sales and Use Tax (STC): `<UT-STC-ACCT>`
- Sales Transient Room (STR): `<UT-STR-ACCT>`

### Sales and Use Tax workflow

1. Authenticate in TAP.
2. Select the **STC** account.
3. Confirm the period/frequency displayed by TAP.
4. Use the current `File now` / `File, view, or amend returns` workflow.
5. Use the return type/account structure TAP assigns:
   - TC-62M for multiple places of business where applicable, or
   - TC-62S for a single place of business where applicable.
6. Do not choose based only on portfolio size; follow the account/outlet configuration.
7. Verify outlet/location codes and current local rates.
8. Reconcile to the filing packet.
9. Stop for Gate 2 before submit/payment.

### Sales Transient Room workflow

1. Select the **STR** account.
2. Confirm the period/frequency displayed by TAP.
3. File transient room tax on the current TC-62T workflow.
4. Verify each outlet/location and rate for the filing period.
5. For Washington County periods beginning July 1, 2026, current Utah Bulletin 8-26 says the county transient room tax increased from 4.25% to 4.5%; still verify the live location/rate matrix.
6. Reconcile to the filing packet.
7. Stop for Gate 2 before submit/payment.

### Utah zero return / rate control

The user-supplied Utah account letter instructs the business to file every filing period and tax type even if no tax is due and to check current rates because rates may change quarterly. Follow the live account schedule.
