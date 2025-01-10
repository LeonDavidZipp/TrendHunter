from pydantic import BaseModel
from src.models import Action
from datetime import datetime


class Sentiment(BaseModel):
    """
    Sentiment to buy a certain cryptocurrency
    """

    source: str = None
    token: str = None
    token_address: str = None
    action: Action = None
    date: datetime = None