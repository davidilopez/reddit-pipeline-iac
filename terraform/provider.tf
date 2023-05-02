terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">=4.60.2"
    }
  }
}

provider "google" {
  region  = var.region
  project = var.project_id
}
