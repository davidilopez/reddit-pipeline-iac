# Spooky Story Pipeline Platform
## Introduction
For this project, I aimed to provision the infrastructure with Terraform to run a Kubernetes cluster with the following elements:
- A pipeline to extract Reddit posts from the most popular horror subreddits and place them in Google Cloud Storage.
- A data warehouse in Apache Druid to store the Reddit posts.
- An analytics platform in Apache Superset to visualize the Reddit posts.
- An orchestrator in Dagster to run the pipeline.

Unfortunately, I ran into some time constraints, namely that I assigned 8 hours for tasks that are still relatively new to me. I was able to complete the following:
- Provision the infrastructure with Terraform.
- Create an API in Python to extract Reddit posts from the most popular horror subreddits.
- A service in Cloud Run to run the API.
- A scheduler in Cloud Scheduler to run the API every 72 hours.
- An empty BigQuery dataset to store the Reddit posts.

I was not able to complete the following:
- Connect the BigQuery dataset to the Google Cloud Storage bucket.
- Provision Apache Superset for visualization.

## Running the project
### Prerequisites
- Terraform
- Docker
- Google Cloud SDK
- Python 3.10
- Pipenv
- Taskfile

### Provisioning the infrastructure
1. Use `terraform init` and `terraform apply` to provision the infrastructure. Some elements might fail on the first run. We will fix these problems in the next steps.
2. Build and upload the API image to Google Artifact Registry with `task upload/api`.
3. Deploy the service with `task deploy/service`. For this, you will need a `.env` file in the `reddit_scraper` directory with a `CLIENT_ID` and a `SERVICE_TOKEN` from Reddit. You can get these by creating a Reddit app [here](https://www.reddit.com/prefs/apps).
4. Re-run `terraform apply` to provision the infrastructure again. This should fix the problems from the first run.
