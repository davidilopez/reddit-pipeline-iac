resource "google_storage_bucket" "reddit_data_lake" {
  name          = "reddit-data-lake"
  location      = var.region
  storage_class = "STANDARD"
  project       = google_project.fedex_project.name
  force_destroy = true
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset
  project    = google_project.fedex_project.name
  location   = var.region

  depends_on = [google_project_service.bigquery]
}

resource "google_bigquery_table" "table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "reddit_posts"
  project    = google_project.fedex_project.name

  schema = <<EOF
[
  {
    "name": "id",
    "type": "STRING"
  },
  {
    "name": "url",
    "type": "STRING"
  },
  {
    "name": "title",
    "type": "STRING"
  },
  {
    "name": "author",
    "type": "STRING"
  },
  {
    "name": "name",
    "type": "STRING"
  },
  {
    "name": "score",
    "type": "INTEGER"
  },
  {
    "name": "num_comments",
    "type": "INTEGER"
  },
  {
    "name": "selftext",
    "type": "STRING"
  },
  {
    "name": "created_utc",
    "type": "TIMESTAMP"
  },
  {
    "name": "created_date",
    "type": "DATE"
  },
  {
    "name": "subreddit",
    "type": "STRING"
  }
]
EOF

  depends_on = [google_bigquery_dataset.dataset]
}
