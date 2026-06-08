# Lab 3.4 Policies

This folder contains Conftest/OPA Rego policies for evaluating Terraform plan JSON.

## Cloud Target Mapping

| Policy file | Cloud | Control | Purpose |
| --- | --- | --- | --- |
| `sc28_encryption_aws.rego` | AWS | SC-28 | Verifies each `aws_s3_bucket` has a matching server-side encryption configuration. |
| `ac3_no_public_aws.rego` | AWS | AC-3 | Verifies each `aws_s3_bucket` has a complete public access block. |
| `cm6_required_tags_aws.rego` | AWS | CM-6 | Verifies supported AWS resources include required governance tags. |

## Evidence Files

The Lab 3.4 evidence artifacts are expected at:

| Evidence file | Purpose |
| --- | --- |
| `evidence/lab-3-4/conftest-pass.json` | Captures Conftest results for the compliant Terraform plan. |
| `evidence/lab-3-4/conftest-fail.json` | Captures Conftest results for the intentionally broken Terraform plan. |

## Example Commands

Run the AWS policy namespaces against a compliant plan:

```bash
conftest test --policy policies --namespace compliance.sc28_aws plan.json
conftest test --policy policies --namespace compliance.ac3_aws plan.json
conftest test --policy policies --namespace compliance.cm6_aws plan.json
```

Run SC-28 against the intentionally broken plan:

```bash
conftest test --policy policies --namespace compliance.sc28_aws broken/plan.json
```
