import pandas as pd
from datetime import datetime
import requests


class SentimentValidator:
    """
    Methods for calculating the influence of a source's sentiments on token prices.
    """
    def __init__(self, df: pd.DataFrame):
        """
        :param df: dataframe containing the sentiment data
        """
        self.df = df

    def _get_token_price_time_series(self, token_addr: str, start: datetime) -> pd.DataFrame:
        """
        Gets a time series of a token's price
        :param start:
        :return:
        """

        # TODO: remove placeholder
        # URL to make the GET request to
        url = 'https://actual_url_here.com/...'

        # Make the GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Process the response content
            data = response.json()
        else:
            # Handle the error
            data = []
        # placeholder end

        # TODO: data processing
        df = pd.DataFrame(data)

        return df

    # to analyze the token price development in relation to the sentiment
    def _name_later(self, token_price_df: pd.DataFrame):
        df = pd.merge(
            self.df,
            token_price_df,
            on="date",
            how="outer" # keep all dates
        )