# Lab 5.2 — AWS Detective Controls Baseline (CGEP)

Deploys an AWS account-level audit and monitoring baseline with Terraform:

- **CloudTrail** — multi-region management-event trail (`cgep-lab-mgmt`) with log file validation, delivered to a dedicated encrypted S3 bucket
- **Security Hub** — enabled with the AWS Foundational Security Best Practices and NIST 800-53 Rev. 5 standards
- **AWS Config** — configuration recorder for resource inventory and change tracking (dependency for many Security Hub controls)

## NIST 800-53 Control Mapping

### CloudTrail → AU-2, AU-12, AU-10

| Control | How it's satisfied |
|---|---|
| **AU-2 (Event Logging)** | The multi-region trail captures all AWS management API events (who, what, when, where) across every region, including global service events. |
| **AU-12 (Audit Record Generation)** | CloudTrail generates audit records for account activity and delivers them to the dedicated S3 bucket (`trail_bucket` output), providing a durable, centralized audit record store. |
| **AU-10 (Non-repudiation)** | `enable_log_file_validation = true` produces signed digest files, allowing cryptographic verification that delivered log files were not modified or deleted after delivery. |

### Security Hub → RA-5, SI-4

| Control | How it's satisfied |
|---|---|
| **RA-5 (Vulnerability Monitoring and Scanning)** | Security Hub continuously evaluates the account against FSBP and NIST 800-53 standards, producing findings (`evidence/lab-5-2/security-hub-findings.json`) that identify misconfigurations and weaknesses with severity ratings. |
| **SI-4 (System Monitoring)** | Security Hub aggregates and normalizes findings from AWS services into a single pane, with `auto_enable_controls = true` ensuring new controls are monitored automatically as standards evolve. |

### AWS Config → CM-2, CM-6, CM-8

| Control | How it's satisfied |
|---|---|
| **CM-2 (Baseline Configuration)** | Config records the configuration state of resources, establishing a point-in-time baseline that subsequent changes are tracked against. |
| **CM-6 (Configuration Settings)** | Config rules (and the Security Hub controls that depend on them) check recorded resource configurations against required settings, flagging drift from approved values. |
| **CM-8 (System Component Inventory)** | The configuration recorder maintains a continuously updated inventory of AWS resources in the account, including relationships and change history. |

## Layout

```
terraform/baselines/aws/
├── main.tf            # providers, default tags, shared data sources
├── variables.tf       # aws_region
├── cloudtrail.tf      # trail + encrypted/private S3 log bucket + bucket policy
├── security_hub.tf    # hub + FSBP and NIST 800-53 standards subscriptions
├── outputs.tf         # trail_name, trail_bucket, hub_arn
└── evidence/lab-5-2/  # captured evidence (Security Hub findings, etc.)
```

## Deploy

```bash
cd terraform/baselines/aws
eval "$(aws configure export-credentials --profile default --format env)"
terraform init
terraform apply -auto-approve
```

## Verify / Capture Evidence

```bash
# CloudTrail is logging
aws cloudtrail get-trail-status --name cgep-lab-mgmt --region us-east-1

# Security Hub is enabled
aws securityhub describe-hub --region us-east-1

# Capture findings as evidence
mkdir -p evidence/lab-5-2
aws securityhub get-findings --region us-east-1 --max-results 50 \
  > evidence/lab-5-2/security-hub-findings.json
```
