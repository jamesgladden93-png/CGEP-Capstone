# Lab 4.4 — Signed Evidence Chain of Custody

## Overview

Every `grc-gate` workflow run bundles its compliance evidence (`plan.json`, `plan.txt`,
`conftest-results.json`, `tfsec.sarif`), signs it with Cosign keyless signing, and uploads
it to an Object Lock–protected S3 evidence vault
(`cgep-lab-grc-evidence-vault-f43675c5`) under `runs/<run_id>/`.

Verification is performed by `scripts/verify-evidence.sh <run_id>`, which exits non-zero
if any link in the chain is broken.

## Chain Property → Proving Artifact

| Chain Property | Artifact | How It Proves the Property |
|---|---|---|
| **Authenticity** | `evidence-<run_id>-<sha>.tar.gz.sig.bundle` (Cosign signature bundle) | The bundle was signed keylessly via GitHub Actions OIDC. The short-lived signing certificate embeds the workflow identity (`https://github.com/jamesgladden93-png/CGEP-Capstone/...`) and the issuer (`https://token.actions.githubusercontent.com`). `cosign verify-blob` rejects any signer that is not this repository's workflow, proving *who* produced the evidence. |
| **Integrity** | `evidence-<run_id>-<sha>.tar.gz.sha256` (digest sidecar) + the Cosign signature over the bundle bytes | The SHA-256 sidecar pins the exact bytes of the bundle; the signature is computed over the same digest. Changing a single byte changes the digest, so both the hash comparison and `cosign verify-blob` fail (demonstrated in the tamper test), proving the evidence is *unmodified*. |
| **Timeliness** | Rekor transparency-log entry inside the `.sig.bundle` + `captured_at`/run metadata in `receipt.json` | Keyless signing records the signature in the Sigstore Rekor transparency log with a counter-signed timestamp at signing time. Combined with the GitHub run ID and commit SHA in `receipt.json`, this proves *when* the evidence was produced and ties it to a specific CI run and commit. |
| **Preservation** | S3 Object Lock retention on the vault object (checked via `aws s3api get-object-retention`) + `version_id` in `receipt.json` | The vault bucket has versioning and Object Lock default retention enabled, and its bucket policy denies deletion to everyone except the account root. The recorded `VersionId` pins the immutable object version; `verify-evidence.sh` fails if `RetainUntilDate` has lapsed, proving the evidence *cannot be altered or destroyed* within its retention window. |

## Tamper Test Result

Appending a single line (`echo "junk" >>`) to a downloaded copy of the bundle:

- Changed the SHA-256 from `4f606a8f…692ee879` to `9012e950…a0eb0e55` → integrity check fails.
- Caused `cosign verify-blob` to exit 1 (`matching bundle to payload` mismatch) → authenticity check fails.

The vault copy itself remains pristine and retention-locked. Chain of custody is
mathematical, not aspirational.

## Verifying a Run

```bash
EVIDENCE_VAULT=cgep-lab-grc-evidence-vault-f43675c5 \
  bash scripts/verify-evidence.sh <run_id> --profile <your-sandbox-profile>
# expected: "CHAIN INTACT for run <run_id>"
```
