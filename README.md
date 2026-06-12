# Lab 5.4 — GCP Security Services Baseline (CGEP)

Terraform baseline for a GCP project covering three preventative/detective layers:

- **Org Policy** (project scope) — reject misconfigurations at the API call
- **Workload Identity Federation** — keyless GitHub Actions auth via OIDC
- **Data Access audit logs** — for Cloud Storage, Cloud KMS, and IAM

Project: `lab-24-grcengineer` (project number `870067517337`)

## The #1 Lesson: Data Access Logs Are OFF by Default

GCP only enables Admin Activity audit logs out of the box. **Data Access logs
(DATA_READ, DATA_WRITE, ADMIN_READ) are off by default** — meaning by default
there is no record of who read which object, used which key, or listed which
service accounts. This is the most-cited GCP audit finding because nobody turns
them on.

This lab enables all three log types for `storage.googleapis.com`,
`cloudkms.googleapis.com`, and `iam.googleapis.com` via
`google_project_iam_audit_config` (see `terraform/baselines/gcp/audit_logs.tf`).
The resulting configuration is captured in `evidence/lab-5-4/iam-policy.json`
under `auditConfigs` — this feeds the OSCAL component's AU-2 implementation
statement.

Cost note: Data Access logs bill at $0.50/GB ingested. Fine for a lab project;
in a busy project, start with one service before enabling all three.

## NIST 800-53 Control Mapping

| Layer | Controls | How |
|---|---|---|
| Org Policy `storage.uniformBucketLevelAccess` | CM-6 | Bucket ACL misconfigurations rejected at the API |
| Org Policy `iam.disableServiceAccountKeyCreation` | AC-2 | Long-lived credentials cannot be minted |
| Org Policy `compute.requireOsLogin` | AC-3 | VM access bound to IAM identities |
| Workload Identity Federation | AC-2, IA-5 | No JSON keys; short-lived OIDC-exchanged tokens, repo-pinned |
| Data Access audit logs | AU-2, AU-12 | Per-service DATA_READ/DATA_WRITE/ADMIN_READ record generation |

## Finding: Org Policy Requires an Organization

The org policy resources in `org_policy.tf` are correct HCL, but **could not be
applied** in this environment:

```
Error 403: Permission 'orgpolicy.policies.create' denied on resource
'//cloudresourcemanager.googleapis.com/projects/lab-24-grcengineer'
```

Root cause: `lab-24-grcengineer` is a **standalone project** (no `parent`
organization, personal Gmail account). The required role
`roles/orgpolicy.policyAdmin`:

- can only be granted at the **organization** level (confirmed:
  `Role roles/orgpolicy.policyAdmin is not supported for this resource` when
  attempting a project-level grant), and
- its permissions are **blacklisted from custom roles** (confirmed:
  `Permission orgpolicy.policies.create is not supported in custom roles`).

Project Owner does not include the permission. With no organization node in the
hierarchy, no principal can ever hold it — Org Policy management is structurally
impossible on a standalone project. Remediation path: create an organization via
Cloud Identity (requires a verified domain), migrate the project under it, and
grant `orgpolicy.policyAdmin` at org level. The Terraform then applies unchanged.

This is itself a GRC lesson: standalone projects cannot self-govern with
preventative API-level controls; the org node is the trust anchor.

## Workload Identity Federation (Keyless CI)

`wif.tf` provisions:

- Pool `github-actions` and OIDC provider for `token.actions.githubusercontent.com`
- `attribute_condition = assertion.repository == "jamesgladden93-png/CGEP-Capstone"`
  — without this, any public GitHub repo could impersonate the service account
- Service account `cgep-grc-gate-sa` with `roles/viewer` only
- `roles/iam.workloadIdentityUser` binding scoped to the repo via `principalSet`

The demo workflow at `.github/workflows/gcp-wif-demo.yml` authenticates with
`google-github-actions/auth@v2` — **no service account JSON keys anywhere**.
Tokens are minted at job start and expire within an hour.

## Layout

```
terraform/baselines/gcp/
├── main.tf            # providers (user_project_override for orgpolicy API), variables
├── org_policy.tf      # 3 project-scope org policies (blocked; see Finding above)
├── wif.tf             # WIF pool, provider, SA, bindings
├── audit_logs.tf      # Data Access logs for storage/kms/iam
└── outputs.tf         # wif_provider, gha_service_account
.github/workflows/
└── gcp-wif-demo.yml   # keyless auth demo
evidence/lab-5-4/
├── iam-policy.json    # auditConfigs evidence (AU-2)
└── wif-outputs.json   # provider + SA identifiers
```

## Deploy

```bash
cd terraform/baselines/gcp
gcloud auth application-default login
gcloud auth application-default set-quota-project lab-24-grcengineer
terraform init
terraform apply -auto-approve -var="gcp_project=lab-24-grcengineer"
```

## Verify

```bash
# WIF pool exists
gcloud iam workload-identity-pools list --location=global --project=lab-24-grcengineer

# Data Access logs enabled
gcloud projects get-iam-policy lab-24-grcengineer --format=json \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); print(json.dumps(d.get("auditConfigs",[]),indent=2))'

# Org policies (empty on standalone project; see Finding)
gcloud org-policies list --project=lab-24-grcengineer
```
