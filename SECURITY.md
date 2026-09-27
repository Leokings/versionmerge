# Security

## Controls

- concrete GenVM runner and Python dependencies are pinned;
- owner and author wallets must be distinct and author addresses nonzero;
- each author can submit exactly one bounded version from their own wallet;
- analysis cannot begin until both versions are present;
- model output uses an exact closed schema and one bounded relation code per section;
- exact-text relationships cannot be contradicted by the model;
- only the owner can propose a conflict choice;
- every final document requires one approval from each author;
- all deployed source bytes and required schema methods are checked against StudioNet.

## Threat boundary

Policies and sections are untrusted and delimited in the prompt. Output normalization and deterministic exact-text checks remain authoritative. Colluding wallets can approve misleading content; the contract records consent but cannot establish real-world identity, authorship, authority, or correctness.

An author may withhold a submission or approval. Because the contract holds no funds and merge records are independently keyed, this is a liveness limitation rather than an asset-loss risk.

## Public-data warning

All versions, policies, and approvals are public. Do not submit confidential drafts, personal data, credentials, or secrets.
