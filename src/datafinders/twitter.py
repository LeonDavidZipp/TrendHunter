import twint
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from src.datafinders.terms import CRYPTO_TERMS
from src.datafinders.constants import LIKE_THRESHOLD, RETWEET_THRESHOLD, REPLY_THRESHOLD
"""
tweet data frame structure:
_data = {
    "id"
    "conversation_id"
    "created_at"
    "date"
    "timezone"
    "place"
    "tweet"
    "language"
    "hashtags"
    "cashtags"
    "user_id"
    "user_id_str"
    "username"
    "name"
    "day"
    "hour"
    "link"
    "urls"
    "photos"
    "video"
    "thumbnail"
    "retweet"
    "nlikes"
    "nreplies"
    "nretweets"
    "quote_url"
    "search"
    "near"
    "geo"
    "source"
    "user_rt_id"
    "user_rt"
    "retweet_id"
    "reply_to"
    "retweet_date"
    "translate"
    "trans_src"
    "trans_dest"
    }
"""

def get_tweets(name: str) -> pd.DataFrame:
    """
    Get tweets from Twitter for a specific user
    :param name: Twitter username
    :return: twint object
    """

    # Configure twint
    c = twint.Config()
    c.Username = name
    c.Since = (datetime.now() - relativedelta(months=2)).strftime("%Y-%m-%d")
    c.Limit = 100
    c.Search = "|".join(CRYPTO_TERMS)
    c.Pandas = True
    c.Hide_output = True
    c.Store_object = True
    # [...]

    # Run twint
    twint.run.Search(c)

    # get dataframe
    df: pd.DataFrame = twint.storage.panda.Tweets_df
    df = df[[
        "conversation_id",
        "created_at",
        "date",
        "tweet",
        "hashtags",
        "cashtags",
        "user_id",
        "user_id_str",
        "username",
        "name",
        "day",
        "link",
        "urls",
        "photos",
        "video",
        "retweet",
        "nlikes",
        "nreplies",
        "nretweets",
        "search",
        "near",
        "geo",
        "source",
    ]]

    # Apply thresholds
    df = df[
        df["nlikes"] > LIKE_THRESHOLD & \
        df["nretweets"] > RETWEET_THRESHOLD & \
        df["nreplies"] > REPLY_THRESHOLD
    ]

    return df