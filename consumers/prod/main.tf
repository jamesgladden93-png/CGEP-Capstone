# consumers/prod/main.tf
module "data_bucket" {
  source = "../../modules/compliant-gcs-bucket"

  gcp_project        = "lab-24-grcengineer"
  project_label      = "cgep-lab"
  environment        = "prod"
  retention_days     = 365
  bucket_name_suffix = "prod-data-001"
}