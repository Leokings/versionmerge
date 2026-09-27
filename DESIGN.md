# Design

## Mechanism

VersionMerge aligns 2–12 public text sections across a base, left version, and right version. Validator output is restricted to one integer relation code per section. Contract code deterministically verifies all exact-text cases and rejects contradictory model output.

Relations 0–3 select base, left, or right deterministically. Relation 4 records a conflict. The owner must select base, left, or right for each conflict, but the selection has no effect until both original authors approve the complete merge.

## State machine

`AWAITING_VERSIONS` → `READY` after both immutable author submissions → `CONFLICTS` or `AWAITING_APPROVAL` after consensus analysis → `AWAITING_APPROVAL` after all conflict choices → `SEALED` after both author approvals.

## On-chain responsibilities

- enforce distinct owner and author roles;
- bind each version to the submitting author wallet;
- bound and normalize all public text;
- reach consensus on semantic section relations;
- verify exact textual relations deterministically;
- require explicit conflict choices and bilateral final approval.

## Off-chain responsibilities

Identity verification, copyright checks, private drafting, rich diff rendering, notifications, and legal reliance remain off-chain.
