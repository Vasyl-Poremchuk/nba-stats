from collectors.base_collector import BaseCollector


class SeasonCollector(BaseCollector):
    """A class to collect data for seasons.

    :param url: A URL of the appropriate season.
    :param encoding: The encoding of the data.
    """

    def __init__(self, url: str, encoding: str = "utf-8") -> None:
        """Construct all necessary attributes for the `SeasonCollector`
        object.

        :param url: A URL of the appropriate season.
        :param encoding: The encoding of the data.
        """
        super().__init__(encoding=encoding)
        self.url = url
