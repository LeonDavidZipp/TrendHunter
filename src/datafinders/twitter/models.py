from src.models import Source

class TwitterSource(Source):
    """
    Data for a Twitter source
    """

    def __init__(self, name: str, id: str):
        super().__init__(name)
        self.id: str = id