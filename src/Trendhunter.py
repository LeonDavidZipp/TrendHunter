from src.algorithms.models import Source, SourceType

class TrendHunter:
    def __init__(self):
        self.sources: dict[SourceType, list[Source]] = {
            SourceType.TWITTER: [],
            SourceType.TELEGRAM: [],
            SourceType.DISCORD: [],
            SourceType.GITHUB: [],
            SourceType.FARCASTER: [],
            SourceType.LENSTER: [],
        }