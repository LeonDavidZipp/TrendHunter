from src.datafinders.twitter.TwitterSentimentFinder import TwitterSentimentFinder
from src.models import SourceType, Source
from src.datafinders.twitter.models import TwitterSource

class SentimentFinder:
    """
    Class to find sentiment of tweets from different sources
    """

    def __init__(
            self,
            twitter_sentiment_finder: TwitterSentimentFinder
    ):
        # twitter sentiment finder
        self.twitter_sentiment_finder = twitter_sentiment_finder
        # other finders
        # [...]
        # sources to scrape for information
        self.sources: dict[SourceType, list[Source]] = {
            SourceType.TWITTER: [],
            SourceType.TELEGRAM: [],
            SourceType.DISCORD: [],
            SourceType.GITHUB: [],
            SourceType.FARCASTER: [],
            SourceType.LENSTER: [],
        }
        self.twitter_sources = dict[str, list[TwitterSource]]
        # self.telegram_sources = dict[str, list[TwitterSource]]
        # self.discord_sources = dict[str, list[TwitterSource]]
        # self.github_sources = dict[str, list[TwitterSource]]
        # self.farcaster_sources = dict[str, list[TwitterSource]]
        # self.lenster_sources = dict[str, list[TwitterSource]]

    def get_twitter_observations(self):
        """
        Get twitter sentiments
        :return: list of sentiments
        """
        return self.twitter_sentiment_finder.run_single()