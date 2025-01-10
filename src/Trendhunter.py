from src.algorithms.models import Source, SourceType

class TrendHunter:
    def __init__(self):
        self.sources: dict[SourceType, list[Source]] = {
            SourceType.TWITTER: [],
            SourceType.REDDIT: [],
            SourceType.NEWS: [],
            SourceType.FORUM: [],
            SourceType.BLOG: [],
            SourceType.YOUTUBE: [],
            SourceType.TELEGRAM: [],
            SourceType.DISCORD: [],
            SourceType.TIKTOK: [],
            SourceType.INSTAGRAM: [],
            SourceType.FACEBOOK: [],
            SourceType.LINKEDIN: [],
            SourceType.GITHUB: [],
            SourceType.MEDIUM: [],
            SourceType.STACKOVERFLOW: [],
            SourceType.SLACK: [],
            SourceType.OTHER: []
        }