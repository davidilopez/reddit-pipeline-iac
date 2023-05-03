resource "google_project" "fedex_project" {
  name            = var.project_id
  project_id      = var.project_id
  billing_account = var.billing_account
}

resource "google_artifact_registry_repository" "reddit_scraper_repository" {
  repository_id = "reddit-scraper"
  format        = "DOCKER"
  location      = var.region
  project       = google_project.fedex_project.name

  depends_on = [google_project_service.artifact]
}

resource "google_cloud_run_v2_service" "reddit_scraper_api" {
  name     = "reddit-scraper-api"
  location = var.region
  project  = google_project.fedex_project.name

  template {
    containers {
      image = "${var.region}-docker.pkg.dev/${google_project.fedex_project.name}/${google_artifact_registry_repository.reddit_scraper_repository.name}/reddit-scraper-api:latest"
    }
  }

  depends_on = [google_project_service.run]
}

resource "google_cloud_scheduler_job" "job" {
  name     = "run-reddit-scraper"
  schedule = "0 0 */3 * *"

  retry_config {
    retry_count = 1
  }

  http_target {
    http_method = "GET"
    uri         = google_cloud_run_v2_service.reddit_scraper_api.uri
  }

  depends_on = [google_project_service.scheduler, google_cloud_run_v2_service.reddit_scraper_api]
}
