import datetime as dt
import os
from typing import List

import structlog
from fastapi import FastAPI
from src.functions import extract_subreddit_data, insert_subreddit_data_to_pg

logger = structlog.get_logger()

app = FastAPI()

pg_url = os.getenv("PG_URL")


@app.get("/")
async def main(subreddits: List[str] = None):
    base_path = "gcs://reddit-data-lake"
    now = dt.datetime.now(dt.timezone.utc)

    # timestamps that define window of posts
    after = int((dt.datetime.now() - dt.timedelta(hours=72)).timestamp())
    before = int(dt.datetime.now().timestamp())

    df = extract_subreddit_data(before=before, after=after, subreddits=subreddits)

    # save data to parquet format
    try:
        insert_subreddit_data_to_pg(df=df, table_name="reddit_posts", pg_url=pg_url)
        logger.info("Data saved to Postgres")
        return {"status": "success"}
    except Exception as e:
        logger.error("Error saving data to Postgres", e=e)
        return {"status": "failed"}
