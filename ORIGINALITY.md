# Originality audit

The final source was compared against 161 GenLayer
contract sources in the workspace. All twenty new target contracts were excluded
from the pre-existing comparison pool.

Nearest pre-existing source: `fundpurposefit\contracts\purpose_cap_ledger.py`

Combined structural score: `0.172149`

Token score: `0.284664`

AST score: `0.08519`

Nearest contract in this new set: `sequencecompressor\contracts\sequence_compressor.py` with combined
score `0.32164`. That score reflects shared safe GenLayer
boilerplate. The mechanisms differ materially:

- This repository: Consensus classifies each base-left-right section relation; deterministic auto-merge handles non-conflicts while bilateral approval gates explicit conflict choices.
- Other repository: Consensus labels every ordered entry from a closed alphabet; deterministic run-length encoding creates assignable contiguous work segments.

The two do not share the same semantic input, deterministic algorithm, storage
record, state lifecycle, or decision views. Exact source SHA-256 values are also
unique across all twenty repositories. The complete machine-readable reports are
`review-tools/twenty-originality-audit.json` and
`review-tools/twenty-pairwise-audit.json` at the workspace level.

Similarity scoring is a review aid, not a guarantee of a human review outcome.
