from enum import IntEnum
from pydantic import BaseModel
from datetime import datetime


class Action(IntEnum):
    BUY = 0
    SELL = 1
    # HOLD = 2

class CheckedState(IntEnum):
    """
    State of an observation
    """

    # source has not been checked
    UNCHECKED = 0
    # source cannot be checked yet
    CANNOT_CHECK_YET = 1
    # source has been checked
    CHECKED = 2

class SourceType(IntEnum):
    """
    Type of information source
    """

    TWITTER = 0
    REDDIT = 1
    NEWS = 2
    YOUTUBE = 3
    TELEGRAM = 4
    DISCORD = 5
    TIKTOK = 6
    GITHUB = 7
    ONCHAIN = 8
    FARCASTER = 9
    LENSTER = 10
    OTHER = 11

class Sentiment(BaseModel):
    """
    Sentiment to buy a certain cryptocurrency
    """

    source: str = None
    token: str = None
    token_address: str = None
    action: Action = None
    when: datetime = None
    date: datetime = None

class Observation:
    """
    Observation of a sentiment
    """

    def __init__(
            self,
            observed_at: datetime,
            source_type: SourceType,
            sentiment: Action,
            token: str,
            token_addr: str = None,
            price: float = None
    ):
        """
        :param observed_at: time of observation
        :param source_type: name of the source
        :param sentiment: sentiment observed
        :param token: token the sentiment is about
        :param token_addr: address of observed token; might not exist at time of observation
        :param price: price of token at time of observation; might not exist at time of observation
        """

        # source type
        self.source_type: SourceType = source_type
        # sentiment observed at
        self.observed_at: datetime = observed_at
        # price at time of observation
        self.price_at_observation_time: float = price
        # the token the sentiment is about
        self.token: str = token
        # the address of the token the sentiment is about
        self.token_addr: str = token_addr
        # sentiment predicted by the source
        self.predicted_sentiment: Action = sentiment
        # whether sentiment has been checked
        self.checked: CheckedState = CheckedState.UNCHECKED
        # relative correctness score; 0.0 is incorrect, 1.0 is correct
        self.correctness_score: float = 0.0

    # checks the observation if it has not been checked
    def verify(self):
        if self.checked:
            return

        # check non-onchain and non-other sources
        if self.source_type != SourceType.ONCHAIN and self.source_type != SourceType.OTHER:
            pass

        # check onchain sources
        elif self.source_type == SourceType.ONCHAIN:
            pass

        # other sources are auto false
        else:
            self.correctness_score = 0.0

class Source:
    """
    Data for an information source
    """

    def __init__(self, name: str):
        # source name
        self.name: str = name
        # time since the source has been observed
        self.observed_since: datetime = datetime.now()
        # list of observations
        self.observations: list[Observation] = []
        # last verified observation index
        self.last_verified_idx: int = -1
        # >= 0.5 is trustworthy, < 0.5 is untrustworthy; combination of all score below
        self.trusted_score: float = 0.0
        # how impactful the source is
        self.impact_score: float = 0.0
        # how correct the source is
        self.correctness_score: float = 0.0
        # how intense correctly predicted changes were
        self.correct_intensity_score: float = 0.0
        # how intense wrongly predicted changes were
        self.incorrect_intensity_score: float = 0.0
        # how shortly changes follow


    # ---------------------------------------------- #
    # Getters                                        #
    # ---------------------------------------------- #
    def get_name(self) -> str:
        return self.name

    def get_observed_since(self) -> datetime:
        return self.observed_since

    def get_observations(self) -> list[Observation]:
        return self.observations

    def get_last_verified_idx(self) -> int:
        return self.last_verified_idx

    def get_trusted_score(self) -> float:
        return self.trusted_score

    # ---------------------------------------------- #
    # Setters                                        #
    # ---------------------------------------------- #
    def set_observed_since(self, observed_since: datetime):
        self.observed_since = observed_since

    def set_last_verified_idx(self, last_verified_idx: int):
        self.last_verified_idx = last_verified_idx

    def set_trusted_score(self, trusted_score: float):
        self.trusted_score = trusted_score
