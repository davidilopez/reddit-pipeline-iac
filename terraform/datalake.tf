resource "google_storage_bucket" "reddit_data_lake" {
  name          = "reddit-data-lake"
  location      = "EU"
  storage_class = "STANDARD"
  project       = google_project.fedex_project.name
  force_destroy = true
}
