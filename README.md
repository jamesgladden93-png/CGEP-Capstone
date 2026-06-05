# Lab 3.3 CGEP

This lab demonstrates a compliance-as-code feedback loop using Terraform plan JSON and Open Policy Agent (OPA) Rego policies.

## Contents

- `terraform/main.tf` - Google Cloud Terraform fixture used to generate a plan.
- `terraform/plan.json` - Generated Terraform plan JSON evaluated by OPA.
- `policies/` - Rego compliance policies.
- `policies/tests/` - Unit tests for the Rego policies.
- `evidence/lab-3-3/opa-test-results.json` - JSON test evidence from `opa test`.

## Controls

- **SC-28** - Requires GCS buckets to use customer-managed encryption keys.
- **AC-3** - Prevents public GCS access and open management firewall ports.
- **CM-6** - Requires compliance labels on taggable resources.

## Run the policy tests

From the project root:

```bash
opa test -v policies/
```

Expected result:

```text
PASS: 8/8
```

## Regenerate the Terraform plan JSON

From the Terraform directory:

```bash
terraform init
terraform validate
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
```

## Evaluate the plan against policies

From the Terraform directory:

```bash
opa eval -d ../policies -i plan.json data.compliance.sc28.deny --format=pretty
opa eval -d ../policies -i plan.json data.compliance.ac3.deny --format=pretty
opa eval -d ../policies -i plan.json data.compliance.cm6.deny --format=pretty
```

Expected compliant result for each command:

```text
[]
```

## Generate test evidence

From the project root:

```bash
opa test --format=json policies/ > evidence/lab-3-3/opa-test-results.json
```
