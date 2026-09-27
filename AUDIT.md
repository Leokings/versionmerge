# Security and submission audit

Reviewed: 2026-09-27

Scope: `contracts/version_merge.py` at SHA-256 `3617a3b07bf9083bba897923720576bfb4200c016d953b4f76f6713e4c5d281c`, direct and integration tests, review documents, and the exact StudioNet deployment in `deployments/studionet.json`.

## Findings resolved

| Severity | Finding | Resolution |
| --- | --- | --- |
| High | The merge owner could previously supply both versions while merely naming other wallets as authors. | `open_merge` now stores only the base and roles. Each distinct author must submit their own immutable version through `submit_version`. |
| Medium | A conflict-free AI result could previously be sealed by the owner without author consent. | Every analyzed result now requires bilateral `approve_merge` calls. |
| Medium | Analysis could begin without cryptographic evidence that both named authors participated. | State remains `AWAITING_VERSIONS` until both author transactions finalize, then becomes `READY`. |
| Low | Policy and section prompt boundaries could be clearer. | All blocks are explicitly untrusted, delimited, and unable to change the required task or output shape. |
| Coverage | Original tests did not cover author impersonation, replacement, incomplete submissions, or bilateral auto-merge approval. | Direct coverage increased from 4 to 14 tests and the five-validator flow was rerun. |

## Verification results

| Gate | Result |
| --- | --- |
| GenVM lint and semantic validation | PASS |
| Strict typecheck | PASS, zero diagnostics |
| Direct invariant and negative-path tests | PASS, 14 tests |
| Independent local validators | PASS, exactly 5 validators |
| StudioNet owner plus two distinct author wallets | PASS |
| Every StudioNet transaction finalized with successful agreeing-validator execution | PASS |
| Latest-final sealed-state readback | PASS |
| Deployed source byte equality | PASS |
| Deployed schema method verification | PASS |
| Secrets in repository | NONE |

StudioNet contract: `0x42b21323d7c0e3ecF382f8B7ca7dB10fbcff06c0`

Deployment transaction: `0x005973c7f165fffc1e0eefdf2abb22c29139be62deaf2a5dc78b3af771838795`

Intelligent transaction: `0x1b33865dbeab31c2685ec5074116a61c66919f704b87f609d21c0b95a8ad7c9d`

Author submission transactions: `0x22f73301041dcc6b52377d18f6a0fb8fed5d69b83b597fe99c188f05fb66be51`, `0xeb7f9b6c492f1ed30ff7d3bcaca28c055cdeb5e900a40691cc6f07d08997e855`

Author approval transactions: `0xd4eb952ea4c1ff0fd377650515512de5196e317feef71c01db2d4c38c767fb17`, `0x04a9f66117dc5666a11ae808a5964a385e9a6605e53a7ffe5f62ecd0474ee5ff`

Observed state: `{"state":"SEALED","relations":[1,2],"conflicts":[],"authors_submitted":true,"authors_approved":true}`

## Residual trust assumptions

- Wallet participation proves control of an address, not off-chain identity or ownership of the text.
- Validators interpret semantic changes; bilateral approval is the final human-controlled safety gate.
- An author can withhold submission or approval. No funds are locked, and another merge key can be opened.
- StudioNet is a test network.

No known review-blocking source, authorization, state-machine, validation, test, or provenance defect remains. This is a focused engineering audit, not a formal proof or a promise of program acceptance.
