from sqlalchemy import create_engine

import os

import pandas as pd
from datetime import datetime, timedelta

import concurrent.futures
import requests

class TokenPriceInteractor:
    def __init__(self, api_key: str, engine):
        self.api_key = api_key
        self.engine = engine

    def fetch_token_price_time_series(self, coin_id: int, time_start: datetime, time_end: datetime) -> None:
        """
        Collects token data and adds it to database
        :param coin_id: Coin ID of CMC API
        :param time_start: Start time for data collection
        :param time_end: End time for data collection
        :return:
        """

        # Prepare request
        url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/historical"
        headers = {
            "X-CMC_PRO_API_KEY": self.api_key
        }
        body = {
            "id": coin_id,
            "time_start": time_start,
            "time_end": time_end,
            "interval": "daily"
        }
        req = requests.Request(
            method="GET",
            url=url,
            headers=headers,
            data=body
        )
        prep_req = req.prepare()

        # Send request
        with requests.Session() as session:
            response = session.send(prep_req)

        # Process response
        if response.status_code == 200:
            data = response.json()
            quotes = data['data']['quotes']
            # Extract data
            data = []
            for quote in quotes:
                usd_quote = quote["quote"]["USD"]
                data.append({
                    "token_id": token_id,
                    "timestamp": quote["timestamp"],
                    "price": usd_quote["price"],
                    "currency": "USD",
                    "volume_24h": usd_quote["volume_24h"],
                    "market_cap": usd_quote["market_cap"],
                    "circulating_supply": usd_quote["circulating_supply"],
                    "total_supply": usd_quote["total_supply"]
                })

            # Create DataFrame
            df = pd.DataFrame(data)

            # Add to database
            df.to_sql(
                name="token_time_series",
                con=self.engine,
                if_exists="append",index=False
            )

    def fetch_tokens_price_time_series(self, token_ids: list[int], time_start: datetime, time_end: datetime) -> None:
        """
        Collects token data and adds it to database
        :param token_ids: List of token IDs
        :param time_start: Start time for data collection
        :param time_end: End time for data collection
        :return:
        """

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.fetch_token_price_time_series, token_ids, [time_start] * len(token_ids), [time_end] * len(token_ids))

    def get_token_price_time_series(self, id: int) -> pd.DataFrame:
        """
        Get token price time series of a token
        :param id: id of token to get time series of
        :return:
        """

        querie = f"SELECT * FROM token_time_series WHERE id = {id}"
        return pd.read_sql(querie, con=self.engine)

    def get_all_token_price_time_series(self) -> pd.DataFrame:
        """
        Get all token price time series
        :return:
        """

        query = f"SELECT * FROM token_time_series"
        return pd.read_sql(query, con=self.engine)

if __name__ == "__main__":
    db = os.getenv("DB")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))
    api_key = os.getenv("CMC_API_KEY")

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')

    token_id = 1
    end = datetime.now()
    start = end - timedelta(days=1)

    tdi = TokenPriceInteractor(api_key, engine)
    tdi.fetch_tokens_price_time_series()