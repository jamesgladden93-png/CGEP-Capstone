terraform {
  required_version = ">= 1.6"
  required_providers {
    google      = { source = "hashicorp/google", version = "~> 5.0" }
    google-beta = { source = "hashicorp/google-beta", version = "~> 5.0" }
  }
}

provider "google" {
  project               = var.gcp_project
  user_project_override = true
  billing_project       = var.gcp_project
}

provider "google-beta" {
  project               = var.gcp_project
  user_project_override = true
  billing_project       = var.gcp_project
}

variable "gcp_project" {
  type        = string
  description = "GCP project ID. Lab uses your own; set via terraform.tfvars or -var."
}

variable "github_org" {
  type    = string
  default = "jamesgladden93-png"
}

variable "github_repo" {
  type    = string
  default = "CGEP-Capstone"
}
