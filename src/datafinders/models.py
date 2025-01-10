from enum import IntEnum

from pydantic import BaseModel


class Sentiment(BaseModel):
    """
    Sentiment to buy a certain cryptocurrency
    """

    class Action(IntEnum):
        BUY = 0
        SELL = 1
        HOLD = 2
    source: str = None
    token: str = None
    token_address: str = None
    action: Action = None