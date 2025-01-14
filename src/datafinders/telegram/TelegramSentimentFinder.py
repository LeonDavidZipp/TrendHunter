

class TelegramSentimentFinder:
    def __init__(self, telegram_api):
        self.telegram_api = telegram_api

    def find(self, query):
        messages = self.telegram_api.get_messages(query)
        return self._analyze_sentiment(messages)

    def _analyze_sentiment(self, messages):
        # Analyze sentiment of messages
        return messages