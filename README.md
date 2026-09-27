# VersionMerge

VersionMerge is a reusable GenLayer Intelligent Contract for author-attested, three-way semantic section merging. A merge owner supplies the common base and policy, each named author submits their own version from their wallet, validators classify each aligned section, and both authors must approve the resulting document before it is sealed.

## How it works

1. `open_merge` records a bounded base, merge policy, and two distinct nonzero author wallets.
2. Each author calls `submit_version` once. The owner cannot submit or replace an author's version.
3. `analyze_merge` becomes available only after both submissions. Validators classify every section as unchanged, left-only, right-only, same-change, or conflict.
4. Exact textual relationships are checked deterministically. Non-conflicting sections merge automatically; the owner proposes an explicit source choice for each conflict.
5. `approve_merge` requires independent approval from both authors for every result, including a conflict-free merge, before state becomes `SEALED`.

## Public interface

Write methods: `open_merge`, `submit_version`, `analyze_merge`, `propose_conflict_choice`, `approve_merge`

View methods: `get_merge`, `merged_sections`, `conflict_indexes`

## Verification

```text
pip install -r requirements.txt
genvm-lint check contracts/version_merge.py
genvm-lint typecheck contracts/version_merge.py --strict
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5
pytest tests/integration/test_version_merge_consensus.py -q
```

Verified results on 2026-09-27: lint PASS, strict typecheck PASS, 14 direct tests PASS, one five-validator integration flow PASS, and a complete three-wallet StudioNet flow PASS.

StudioNet contract: https://explorer-studio.genlayer.com/address/0x42b21323d7c0e3ecF382f8B7ca7dB10fbcff06c0

The finalized live flow recorded two independent author submissions, validator relations `[1,2]`, two author approvals, the expected merged sections, and final state `SEALED`. See `deployments/studionet.json` for every transaction and the exact source proof.

## Boundary

All versions, policies, approvals, calldata, and results are public. Wallet signatures attest only which on-chain address submitted or approved data; they do not prove a person's identity, copyright ownership, or legal authority. The contract moves no funds.
