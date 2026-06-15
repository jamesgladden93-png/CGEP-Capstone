# Lab 6.1 CGEP - OSCAL Component Definition

## Overview
This directory contains an OSCAL Component Definition for the `compliant-s3` Terraform module, demonstrating how infrastructure-as-code can be documented and assessed using NIST 800-53 Rev 5 controls.

## Component Description

**compliant-s3 v1.0.0**
- **Type:** Software (Terraform Module)
- **Purpose:** Reusable pattern for AWS S3 primary bucket plus dedicated access-log bucket
- **Compliance Features:**
  - Server-side encryption (AES-256) — hardcoded, non-overridable
  - Public access block (all four flags true) — hardcoded
  - Access logging to dedicated log bucket
  - Required compliance tags (Project, Environment, ManagedBy, ComplianceScope)
  - Versioning enabled

## Control Mapping

| Control ID | Description | Evidence Location |
|------------|-------------|-------------------|
| **sc-28** | Protection of Information at Rest | S3 bucket encryption configuration |
| **ac-3** | Access Enforcement | S3 public access block (all four flags) |
| **au-3** | Content of Audit Records | S3 access logging to dedicated log bucket |
| **cm-6** | Configuration Settings | Required tags via AWS provider default_tags |

## Evidence Vault

All evidence is stored in the GRC Evidence Vault with cryptographic verification:

- **Vault:** `s3://cgep-lab-grc-evidence-vault-f43675c5`
- **Run ID:** `27579197994`
- **Bundle:** `evidence-27579197994-a589ac779b780303b535d697e725d034115714d7.tar.gz`
- **Verification:** SHA256 + Cosign signature + S3 retention

### Evidence Traversal

An assessor can verify this component by:

1. **OSCAL Document** → `component-definitions/compliant-s3-v1/component-definition.json`
2. **Evidence Link** → `links[rel=evidence].href` points to S3 vault
3. **Signed Bundle** → Download and verify with `verify-evidence.sh`
4. **Chain Intact** → Integrity, authenticity, and preservation confirmed

## Repository Layout

```
lab-6-1/
├── component-definitions/
│   └── compliant-s3-v1/
│       └── component-definition.json    # OSCAL component (VALID)
├── profiles/
│   └── cge-p-minimum/
│       └── profile.json                  # Control selection profile (VALID)
├── cge-p-minimum-resolved/               # Resolved profile markdown
│   ├── sc/sc-28.md
│   ├── ac/ac-3.md
│   ├── au/au-3.md
│   └── cm/cm-6.md
├── evidence/
│   └── lab-6-1/
│       └── trestle-validate.txt          # Validation output
└── README.md                             # This file

```

## Validation Commands

```bash
# Validate component definition
trestle validate -f component-definitions/compliant-s3-v1/component-definition.json

# Validate profile
trestle validate -f profiles/cge-p-minimum/profile.json

# Generate resolved profile
trestle author profile-generate -n cge-p-minimum -o cge-p-minimum-resolved

# Verify evidence chain
cd ../Lab\ 4.4\ CGEP
EVIDENCE_VAULT=cgep-lab-grc-evidence-vault-f43675c5 bash scripts/verify-evidence.sh 27579197994
```

## NIST 800-53 Rev 5 Catalog Source

```
https://raw.githubusercontent.com/usnistgov/oscal-content/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
```

## Portfolio Submission Checklist

- [x] `component-definitions/compliant-s3-v1/component-definition.json` validated by trestle
- [x] `profiles/cge-p-minimum/profile.json` validated by trestle  
- [x] `evidence/lab-6-1/trestle-validate.txt` captured with validation output
- [x] README explaining component module and evidence location
- [x] Evidence URI resolves to real signed object in vault (run 27579197994)
- [x] Profile resolved to `cge-p-minimum-resolved/` with control markdown
