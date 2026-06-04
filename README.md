# Lab 2.5 CGEP

Lab 2.5 builds an AWS-based evidence vault for capturing, preserving, and proving the integrity of compliance evidence.

## Overview

This lab provisions an S3 evidence vault with controls designed for governance, risk, and compliance workflows:

- S3 bucket with Object Lock enabled at creation
- Bucket versioning enabled
- Default object retention policy
- Server-side encryption using AES-256
- Public access blocked
- Bucket deletion denied except for the account root principal
- Evidence capture script that bundles Terraform evidence and uploads it to the vault

## Project Structure

```text
.
├── evidence/
│   └── Lab-2-5/
│       └── receipt.json
├── scripts/
│   └── capture-evidence.sh
└── terraform/
    ├── main.tf
    ├── outputs.tf
    └── variables.tf
```

## Terraform Resources

The Terraform configuration creates:

- `aws_s3_bucket.vault`
- `aws_s3_bucket_versioning.vault`
- `aws_s3_bucket_object_lock_configuration.vault`
- `aws_s3_bucket_server_side_encryption_configuration.vault`
- `aws_s3_bucket_public_access_block.vault`
- `aws_s3_bucket_policy.vault`
- `random_id.suffix`

## Usage

From the project root:

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply -auto-approve
VAULT=$(terraform -chdir=terraform output -raw vault_name)
```

Then capture evidence:

```bash
bash scripts/capture-evidence.sh \
  --workspace "../Lab 2.3 CGEP" \
  --run-id test-001 \
  --vault "$VAULT" \
  --profile default
```

## Evidence Receipt

The evidence receipt is stored at:

```text
evidence/Lab-2-5/receipt.json
```

It records the run ID, vault bucket, object key, version ID, and capture timestamp.

## Security Notes

Terraform state files are intentionally excluded from version control because they may contain infrastructure metadata. Generated bundles, signature bundles, `.terraform/`, and local editor files are also ignored.

Object Lock is enabled at bucket creation time because it cannot be added later to an existing S3 bucket.

## GitHub Branch

This lab was pushed to the `lab-2.5-cgep` branch of the CGEP Capstone repository.
