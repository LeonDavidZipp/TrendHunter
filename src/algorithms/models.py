from datetime import datetime
from enum import IntEnum


class SourceType(IntEnum):
    """
    Type of information source
    """
    TWITTER = 0
    REDDIT = 1
    NEWS = 2
    FORUM = 3
    BLOG = 4
    YOUTUBE = 5
    TELEGRAM = 6
    DISCORD = 7
    TIKTOK = 8
    INSTAGRAM = 9
    FACEBOOK = 10
    LINKEDIN = 11
    GITHUB = 12
    MEDIUM = 13
    STACKOVERFLOW = 14
    SLACK = 15
    OTHER = 16

class Source:
    """
    Data for an information source
    """

    def __init__(self, name: str):
        self.name: str = name
        self.observed_since: datetime = datetime.now()
        # >= 0.5 is trustworthy, < 0.5 is untrustworthy; trusted by default
        self.trusted_score: float = 0.5