import twint
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from pydantic import BaseModel
from typing import Literal

from openai import OpenAI

import concurrent.futures

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

class TwitterSentiment(BaseModel):
    """
    Twitter sentiment to buy a certain cryptocurrency
    """
    token: str = None
    token_address: str = None
    action: Literal["buy", "sell", "hold"] = None


class TwitterSentimentFinder:
    """
    Class to find sentiment of tweets from Twitter

    """
    def __init__(self):
        self.client = OpenAI()
        self.to_drop = [
            "id",
            "timezone",
            "place",
            "language",
            "hour",
            "thumbnail",
            "quote_url",
            "user_rt_id",
            "user_rt",
            "retweet_id",
            "reply_to",
            "retweet_date",
            "translate",
            "trans_src",
            "trans_dest"
        ]

    def get_user_tweets(self, user: str) -> pd.DataFrame:
        """
        Get tweets from Twitter for a specific user
        :param user: Twitter username
        :return: pandas DataFrame containing tweets
        """

        # Configure twint
        c = twint.Config()
        c.Username = user
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
        df.drop(columns=self.to_drop, inplace=True)

        # Apply thresholds
        df = df[
            (df["nlikes"] > LIKE_THRESHOLD) & \
            (df["nretweets"] > RETWEET_THRESHOLD) & \
            (df["nreplies"] > REPLY_THRESHOLD)
            ]

        return df

    def get_users_tweets(self, users: list[str]) -> pd.DataFrame:
        """
        Get tweets from Twitter for a list of users
        :param users: List of Twitter usernames
        :return: pandas DataFrame containing tweets
        """
        # [...]

        # Get tweets for each user
        dfs = [self.get_user_tweets(user) for user in users]

        return pd.concat(dfs, sort=True, ignore_index=True, copy=False)

    def get_sentiments(self, tweets: pd.DataFrame) -> list[TwitterSentiment]:
        """
        Get sentiment analysis for tweets
        :param tweets: pandas DataFrame containing tweets
        :return: list of TwitterSentiment objects
        """

        def extract_sentiment(entry: str) -> TwitterSentiment:
            try:
                completion = self.client.beta.chat.completions.parse(
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {"role": "system", "content": "Extract the information regarding a token if given."},
                        {"role": "user", "content": entry},
                    ],
                    response_format=TwitterSentiment,
                )
                return completion.choices[0].message.parsed
            except Exception:
                return TwitterSentiment()

        with (concurrent.futures.ThreadPoolExecutor() as executor):
            sentiments = list(executor.map(extract_sentiment, tweets["tweet"].to_list()))

        return sentiments
