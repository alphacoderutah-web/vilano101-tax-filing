# Property / Entity / Government Account Map

**Template.** Use `account-registry.yaml` for exact numbers. This document explains the grouping
logic — which properties roll up to which government filing account, and why.

## Structure to capture per state

```
state -> county -> property -> ownership entity -> operating entity
      -> platform account -> channel -> tax type -> government filing account
```

## Florida pattern

For each county group, record:

- the properties in the group
- the DOR certificate they file under
- the county TDT account they file under
- any property that sits in a **different platform account** from the rest of its filing group

> **Known trap.** A property can belong to one government filing group while living in a
> *different* property-management account. Building a close from one PMS account alone then
> silently understates that return. Always reconcile the full property list against the registry,
> not against whatever one account happens to show.

> **Known trap.** A single physical property may exist as **two** PMS records split by channel
> (for example "X Airbnb Only" and "X Vrbo Only"). Both roll up to one certificate and one county
> account. Any per-property aggregation must combine them or the return is short.

## Utah pattern

Record:

- the properties in the state group
- the entity that owns the TAP accounts
- TAP outlet/location IDs and 5-digit county/city codes **per property**
- the filing frequency shown live in TAP

> Properties in the same county can sit in **different municipalities** with different codes and
> different municipal transient-room rates. Read outlet numbers and city codes off the portal or a
> prior filed return; never assume they are uniform across a portfolio.

## Open-item discipline

Any mapping that has not been confirmed against a live portal or government document should be
recorded here explicitly as an open item, with the date it was last checked.
