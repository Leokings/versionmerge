# VersionMerge

Three-way semantic section merge.

Batch: B

## Why it is GenLayer-native

Consensus classifies each base-left-right section relation; deterministic auto-merge handles non-conflicts while bilateral approval gates explicit conflict choices.

The LLM handles only the bounded semantic step. Deterministic contract code owns
the reusable algorithm, state transitions, access control, tie-breaking, and
views. One deployment supports many caller-keyed records; it is not tied to the
StudioNet fixture or one organization.

## Public interface

Write methods: `open_merge`, `analyze_merge`, `propose_conflict_choice`, `approve_resolutions`, `seal_auto_merge`

View methods: `get_merge`, `merged_sections`, `conflict_indexes`

## Verification

```text
pip install -r requirements.txt
genvm-lint check contracts/version_merge.py
genvm-lint typecheck contracts/version_merge.py --strict
pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5
gltest tests/integration -q --network localnet
```

The live smoke test is opt-in and requires a repository-specific wallet bundle
outside the repository. It waits for finalized receipts, reads `LATEST_FINAL`,
retrieves deployed source and schema from StudioNet, and fails unless the source
bytes exactly match this repository.

StudioNet contract: https://explorer-studio.genlayer.com/address/0xe30747bFEc45E515bE1bB4D95E5997646e347629

See `AUDIT.md`, `ORIGINALITY.md`, `SOURCE_POLICY.md`, `SECURITY.md`,
`SUBMISSION.md`, and `deployments/studionet.json` for the final evidence.

## Boundary

The contract moves no funds and does not establish identity, ownership,
professional authority, source authenticity, physical truth, or legal effect.
All caller inputs and calldata are public. Off-chain clients own authentication,
privacy, source curation, indexing, and the decision to rely on a result.
