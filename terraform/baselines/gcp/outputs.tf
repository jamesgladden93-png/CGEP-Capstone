output "wif_provider" {
  description = "Full resource name of the WIF provider for google-github-actions/auth"
  value       = google_iam_workload_identity_pool_provider.github.name
}

output "gha_service_account" {
  description = "Service account email for GitHub Actions"
  value       = google_service_account.gha.email
}