import datetime as dt
from typing import List

import structlog
from fastapi import FastAPI
from src.functions import extract_subreddit_data

logger = structlog.get_logger()

app = FastAPI()


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
        df.to_parquet(
            f"{base_path}/reddit_data.pq",
            engine="pyarrow",
            compression="snappy",
            partition_cols=["created_date", "subreddit"],
            index=False,
        )

        logger.info("Data saved successfully to parquet format")
        return {"status": "success"}
    except Exception as e:
        logger.error("Error saving data to parquet format", e=e)
        return {"status": "failed"}
