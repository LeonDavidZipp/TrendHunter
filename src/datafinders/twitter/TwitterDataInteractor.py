import twint
from sqlalchemy import create_engine

import pandas as pd
from datetime import datetime

from src.datafinders.terms import CRYPTO_TERMS

import os
import concurrent.futures

class TwitterDataInteractor:
    def __init__(self, db: str, user: str, password: str, host: str, port: int):
        self.engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

    def scrape_user_tweets(self, user_id: int, last_observed: datetime) -> None:
        """
        Get tweets from Twitter for a specific user
        :param user_id: Twitter username
        :param last_observed: Date to look back to
        :return: pandas DataFrame containing tweets
        """

        # Configure twint
        c = twint.Config()
        c.User_id = user_id
        c.Since = last_observed.strftime("%Y-%m-%d")
        c.Limit = 100
        c.Search = "|".join(CRYPTO_TERMS)
        c.Pandas = True
        c.Hide_output = True
        c.Store_object = True
        # [...]

        # Run twint & get tweets df
        twint.run.Search(c)
        df: pd.DataFrame = twint.storage.panda.Tweets_df
        df.rename(columns={"id": "tweet_id"}, inplace=True)
        df['created_at'] = pd.to_datetime(df['created_at'])
        df['date'] = pd.to_datetime(df['date'])
        to_drop = [
            "conversation_id",
            "place",
            "link",
            "urls",
            "photos",
            "video",
            "thumbnail",
            "geo",
            "translate",
            "trans_src",
            "trans_dest"
        ]
        df.drop(columns=to_drop, inplace=True)
        df.sort_values(by="created_at", ascending=True, inplace=True)

        df.to_sql(name="tweets", con=self.engine, if_exists="append", index=False)

    def scrape_users_tweets(self, user_ids: list[int], last_observed: datetime) -> None:
        """
        Get tweets from Twitter for a list of users
        :param user_ids: List of Twitter usernames
        :return: pandas DataFrame containing tweets
        """

        # Get tweets for each user
        l: list[datetime] = [last_observed] * len(user_ids)
        with (concurrent.futures.ThreadPoolExecutor() as executor):
            executor.map(self.get_user_tweets, user_ids, l)

    def get_user_tweets(self, user_id: int) -> pd.DataFrame:
        """
        Get tweets from Twitter for a specific user
        :param user_id: Twitter username
        :return: pandas DataFrame containing tweets
        """

        query = f"SELECT * FROM tweets WHERE user_id = {user_id}"
        return pd.read_sql(query, con=self.engine)

    def get_tweet(self, id: int):
        """
        Gets a tweet of corresponding id
        :param id:
        :return:
        """

        query = f"SELECT * FROM tweets WHERE id = {id}"
        return pd.read_sql(query, con=self.engine)

    def get_all_tweets(self):
        """
        Gets all tweets from within tweet table
        :return:
        """

        query = f"SELECT * FROM tweets"
        return pd.read_sql(query, con=self.engine)

if __name__ == "__main__":
    db = os.getenv("DB")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))

    user_id = 1
    last_observed = datetime.now()

    tdi = TwitterDataInteractor(db, user, password, host, port)
    tdi.scrape_user_tweets(user_id, last_observed)