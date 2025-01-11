from src.models import Source, SourceType
from src.datafinders.SentimentFinder import SentimentFinder

class TrendHunter:
    def __init__(
            self,
            wallets: list[str],
            sentiment_finder: SentimentFinder
    ):
        # wallets to withdraw to
        self.wallets: list[str] = wallets
        # dict of lists of sources to scrape for information
        self.sources: dict[SourceType, list[Source]] = {
            SourceType.TWITTER: [],
            SourceType.TELEGRAM: [],
            SourceType.DISCORD: [],
            SourceType.GITHUB: [],
            SourceType.FARCASTER: [],
            SourceType.LENSTER: [],
        }
        # sell half of invest when initial invest doubles
        self.sell_upper_bound = 1.0
        # sell all invest when initial invest halves
        self.sell_lower_bound = 0.5
        #twitter sentiment finder
        self.sentiment_finder = sentiment_finder

    # ---------------------------------------------- #
    # Getters                                        #
    # ---------------------------------------------- #
    def get_wallets(self) -> list[str]:
        """
        Get the wallets
        :return: all wallets
        """
        return self.wallets

    def get_sources(self) -> dict[SourceType, list[Source]]:
        """
        Get the sources
        :return: all sources
        """
        return self.sources

    def get_sell_upper_bound(self) -> float:
        """
        Get the upper bound for selling
        :return: float
        """
        return self.sell_upper_bound

    def get_sell_lower_bound(self) -> float:
        """
        Get the lower bound for selling
        :return:
        """
        return self.sell_lower_bound

    # ---------------------------------------------- #
    # Setters                                        #
    # ---------------------------------------------- #
    def set_sell_upper_bound(self, upper_bound: float):
        """
        Set the upper bound for selling
        :param upper_bound: float
        """
        self.sell_upper_bound = upper_bound

    def set_sell_lower_bound(self, lower_bound: float):
        """
        Set the lower bound for selling
        :param lower_bound: float
        """
        self.sell_lower_bound = lower_bound

    def check_invest(self):
        """
        Check if the algorithm should invest
        """
        pass

    def check_uninvest(self):
        """
        Check if the algorithm should uninvest
        """
        pass

    def invest(self):
        """
        Invest in a token
        """
        pass

    def uninvest(self):
        """
        Uninvest in a token
        """
        pass

    def withdraw(self):
        """
        Withdraw from a token
        :return:
        """
        pass