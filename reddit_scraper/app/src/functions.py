import datetime as dt
import os
from typing import List

import pandas as pd
import praw
import structlog

logger = structlog.get_logger()

CLIENT_ID = os.getenv("CLIENT_ID")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")


reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=SECRET_TOKEN,
    user_agent="my agent",
)


def extract_subreddit_data(
    before: int, after: int, subreddits: List[str] = None, limit: int = None
) -> pd.DataFrame:
    submissions = []
    if subreddits is None:
        subreddits = [
            "nosleep",
            "creepypasta",
            "shortscarystories",
            "libraryofshadows",
        ]
    if type(subreddits) == str:
        subreddit_posts = reddit.subreddit(subreddits).new(limit=limit)
    else:
        subreddit_posts = reddit.subreddit("+".join(subreddits)).new(limit=limit)
    try:
        for submission in subreddit_posts:
            submission_data = {
                "id": submission.id,
                "url": submission.url,
                "title": submission.title,
                "author": submission.author.name if submission.author else "deleted",
                "name": submission.name,
                "score": submission.score,
                "num_comments": submission.num_comments,
                "selftext": submission.selftext,
                "created_utc": dt.datetime.utcfromtimestamp(submission.created_utc),
                "created_date": dt.datetime.utcfromtimestamp(
                    submission.created_utc
                ).date(),
                "subreddit": submission.subreddit.display_name,
            }
            # check if submission is within time window
            if submission.created_utc > after and submission.created_utc < before:
                submissions.append(submission_data)
    except Exception as e:
        logger.error("Error extracting data from subreddit", e=e)
    return pd.DataFrame(submissions)
