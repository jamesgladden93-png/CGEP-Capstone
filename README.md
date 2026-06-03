# Compliant GCS Bucket Module

This Terraform module deploys a Google Cloud Storage bucket with compliance-focused security defaults enforced inside the module.

## Controls Implemented

| NIST Control | Family | How This Module Implements It |
|---|---|---|
| SC-12 | System and Communications Protection | Creates and manages a customer-managed encryption key using Google Cloud KMS. |
| SC-13 | System and Communications Protection | Uses cryptographic protection through a Cloud KMS key with a 90-day rotation period. |
| SC-28 | System and Communications Protection | Protects data at rest by enforcing default KMS encryption on the GCS bucket. |
| AU-11 | Audit and Accountability | Enables bucket versioning and retention policy to preserve objects for the configured retention period. |
| CM-6 | Configuration Management | Enforces required labels such as project, environment, managed_by, and compliance_scope. |

## Security Defaults

This module enforces:

- Uniform bucket-level access
- Public access prevention
- Default KMS encryption
- Versioning
- Retention policy
- Required compliance labels

## Evidence Output

The module returns a `compliance_attestation` output containing machine-readable evidence for:

- Encryption
- Versioning
- Public access prevention
- Uniform access
- Retention period
- Required labels
- KMS rotation period
