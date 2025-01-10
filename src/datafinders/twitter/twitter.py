import twint
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openai import OpenAI

import concurrent.futures

from src.datafinders.models import Sentiment
from src.datafinders.terms import CRYPTO_TERMS

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


class TwitterSentimentFinder:
    """
    Class to find sentiment of tweets from Twitter
    """

    def __init__(self, like_threshold: int = 0, retweet_threshold: int = 0, reply_threshold: int = 0):
        self.like_threshold = like_threshold
        self.retweet_threshold = retweet_threshold
        self.reply_threshold = reply_threshold
        self.client = OpenAI()

    def _get_user_tweets(self, user_id: int, since: int) -> pd.DataFrame:
        """
        Get tweets from Twitter for a specific user
        :param user_id: Twitter username
        :param since: Number of months to look back
        :return: pandas DataFrame containing tweets
        """

        # Configure twint
        c = twint.Config()
        c.User_id = user_id
        c.Since = (datetime.now() - relativedelta(months=since)).strftime("%Y-%m-%d")
        c.Limit = 100
        c.Search = "|".join(CRYPTO_TERMS)
        c.Pandas = True
        c.Hide_output = True
        c.Store_object = True
        # [...]

        # Run twint & get tweets df
        twint.run.Search(c)
        df: pd.DataFrame = twint.storage.panda.Tweets_df

        # Apply thresholds & drop unnecessary columns
        df = df[
            (df["nlikes"] > self.like_threshold) & \
            (df["nretweets"] > self.retweet_threshold) & \
            (df["nreplies"] > self.reply_threshold)
            ]
        df = df[["user_id", "username", "tweet", "created_at"]]
        df.sort_values(by="created_at", ascending=True, inplace=True)

        return df

    def _get_users_tweets(self, user_ids: list[int], since: int) -> pd.DataFrame:
        """
        Get tweets from Twitter for a list of users
        :param user_ids: List of Twitter usernames
        :return: pandas DataFrame containing tweets
        """
        # [...]

        # Get tweets for each user
        dfs = [self._get_user_tweets(user_id, since) for user_id in user_ids]

        return pd.concat(dfs, sort=True, ignore_index=True, copy=False)

    def _call_openai_for_sentiment(self, content: str, source: str) -> Sentiment:
        try:
            completion = self.client.beta.chat.completions.parse(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system",
                     "content": "Extract the information & buying sentiment for a token if given."},
                    {"role": "user",
                     "content": content},
                ],
                response_format=Sentiment,
            )
            res: Sentiment = completion.choices[0].message.parsed
            res.source = source

            return res
        except Exception:
            return Sentiment()

    def _get_sentiments(self, contents: list[str], users: list[str]) -> list[Sentiment]:
        """
        Get sentiment analysis for tweets
        :param contents: List of tweet contents
        :param users: List of tweet authors
        :return: list of Sentiment objects
        """

        with (concurrent.futures.ThreadPoolExecutor() as executor):
            sentiments = list(executor.map(self._call_openai_for_sentiment, contents, users))

        return sentiments

    def run(self, user_ids: list[int], since: int) -> list[Sentiment]:
        """
        Run the sentiment finder
        :param user_ids: List of Twitter user ids
        :param since: Number of months to look back
        :return: list of TwitterSentiment objects
        """

        tweets = self._get_users_tweets(user_ids, since)
        sentiments = self._get_sentiments(tweets["tweet"].to_list(), tweets["username"].to_list())

        return sentiments

    def run_single(self, user_id: int, since: int) -> list[Sentiment]:
        """
        Run the sentiment finder for a single user
        :param user_id: Twitter user id
        :param since: Number of months to look back
        :return: list of TwitterSentiment objects
        """

        tweets = self._get_user_tweets(user_id, since)
        sentiments = self._get_sentiments(tweets["tweet"].to_list(), tweets["username"].to_list())

        return sentiments