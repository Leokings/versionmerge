# Final audit

Reviewed: 2026-08-25

Scope: `contracts/version_merge.py` at SHA-256 `cc4aabfbdda9601b6d7cda7cf8e4e2d236818d6c04ec7c58d793f01a34ad4f3c`, its
tests and review documents, and the exact StudioNet deployment recorded in
`deployments/studionet.json`.

## Results

| Gate | Result |
| --- | --- |
| GenVM lint and semantic validation | PASS |
| Strict Pyright typecheck | PASS, zero diagnostics |
| Direct invariant tests | PASS, 4 tests |
| Independent GLSim validators | PASS, exactly 5 validators |
| StudioNet deployment | PASS, FINALIZED |
| Real intelligent write | PASS, AGREE or MAJORITY_AGREE |
| Latest-final state readback | PASS |
| Deployed source byte equality | PASS |
| Deployed schema required-method read | PASS |
| Dependency and GenVM runner pins | PASS |
| Prompt-injection boundary and JSON normalization | PASS |
| External wallet isolation | PASS, 5 unique roles for this repository |
| Cross-repository wallet reuse | NONE across 100 roles |
| Private key or mnemonic in repository | NONE |
| Workspace-wide originality scan | PASS, 161 contract sources scanned |
| GitHub destination (2026-08-28 publication update) | Private repository: Leokings/versionmerge |

StudioNet contract: 0xe30747bFEc45E515bE1bB4D95E5997646e347629

Deployment transaction: 0x6784223fba0e9fbef81bd0e2eacabbcdf50da9676adedd6fef3e3136b6a0d51e

Intelligent transaction: 0x298e9b2dc1b8dc9fd23e018faf8e86d6ad5b079f847fe73b6458058366e972e7

Observed live state: `{"conflicts":[],"relations":[1,2],"state":"AUTO_MERGED"}`

## Consensus review

Validators independently re-execute the bounded semantic task and the custom validator rejects malformed or materially different output.

## Review conclusion

No known source, build, test, consensus, wallet, secret, dependency, provenance,
or repository-hygiene blocker remains. Human program review can still apply its
own policy judgment; this audit does not promise acceptance.

Publication note: private GitHub evidence requires reviewer access. The original
StudioNet source and wallets are unchanged. CI uses the server's GET /health route
for readiness; /api is a POST-only JSON-RPC route. No live wallet keys are used by CI.
