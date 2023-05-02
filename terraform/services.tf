resource "google_project_service" "artifact" {
  project = google_project.fedex_project.name
  service = "artifactregistry.googleapis.com"

  disable_dependent_services = true
}

resource "google_project_service" "run" {
  project = google_project.fedex_project.name
  service = "run.googleapis.com"

  disable_dependent_services = true
}

resource "google_project_service" "scheduler" {
  project = google_project.fedex_project.name
  service = "cloudscheduler.googleapis.com"

  disable_dependent_services = true
}
