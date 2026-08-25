Project name: VersionMerge

Category: Intelligent Contracts

Batch: B

One-line description: Three-way semantic section merge.

What it does: Consensus classifies each base-left-right section relation; deterministic auto-merge handles non-conflicts while bilateral approval gates explicit conflict choices.

Why GenLayer: GenLayer consensus performs the bounded semantic step, then deterministic contract code executes and stores the mechanism-specific result.

Reusable: Yes. One deployment supports many independently keyed records and callers; the live fixture is only an example.

Repository: Standalone local repository. No GitHub remote is configured and nothing was pushed.

Contract source: contracts/version_merge.py

Source SHA-256: cc4aabfbdda9601b6d7cda7cf8e4e2d236818d6c04ec7c58d793f01a34ad4f3c

StudioNet contract: https://explorer-studio.genlayer.com/address/0xe30747bFEc45E515bE1bB4D95E5997646e347629

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x6784223fba0e9fbef81bd0e2eacabbcdf50da9676adedd6fef3e3136b6a0d51e

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x298e9b2dc1b8dc9fd23e018faf8e86d6ad5b079f847fe73b6458058366e972e7

Verification: GenVM lint PASS; strict typecheck PASS; 4 direct tests PASS; five-validator GLSim PASS; finalized StudioNet intelligent write and latest-final readback PASS; exact deployed-source and schema verification PASS.

Originality: Compared with 161 workspace contract sources. Nearest pre-existing structural score is 0.172149; mechanism and source hash are distinct.

Data boundary: Caller-supplied public data only. No external source fetching, funds, identity attestation, legal effect, or private-data guarantee.
