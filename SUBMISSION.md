Project name: VersionMerge

Category: Intelligent Contracts

One-line description: Author-attested three-way semantic merging with bilateral final approval.

What it does: A merge owner records the base and two author wallets. Each author submits their own immutable version. GenLayer validators classify aligned section relationships, deterministic code builds the merge, and both authors must approve before sealing.

Why GenLayer: Semantic equivalence and conflict classification need validator intelligence; provenance, exact-text checks, authorization, conflict choices, and approval state are enforced deterministically on-chain.

Repository: https://github.com/Leokings/versionmerge

Contract source: `contracts/version_merge.py`

Source SHA-256: `3617a3b07bf9083bba897923720576bfb4200c016d953b4f76f6713e4c5d281c`

StudioNet contract: https://explorer-studio.genlayer.com/address/0x42b21323d7c0e3ecF382f8B7ca7dB10fbcff06c0

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x005973c7f165fffc1e0eefdf2abb22c29139be62deaf2a5dc78b3af771838795

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x1b33865dbeab31c2685ec5074116a61c66919f704b87f609d21c0b95a8ad7c9d

Verification: lint PASS; strict typecheck PASS; 14 direct tests PASS; five-validator integration PASS; complete finalized three-wallet StudioNet flow PASS; latest-final sealed readback PASS; deployed-source and schema equality PASS.

Data boundary: Public caller-supplied text only. Wallet control is not proof of identity, copyright ownership, or legal authority.
