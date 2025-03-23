from pathlib import Path

from collectors.base_collector import BaseCollector
from common.constants import BaseConstants, LeagueConstants, SeasonConstants


class LeagueCollector(BaseCollector):
    """A class to collect data for leagues.

    :param encoding: The encoding of the data.
    """

    def __init__(self, encoding: str = "utf-8") -> None:
        """Construct all necessary attributes for the `LeagueCollector`
        object.

        :param encoding: The encoding of the data.
        """
        super().__init__(encoding=encoding)

    @staticmethod
    def get_league_filepath(season_url: str) -> Path:
        """Get a filepath of the league based on the specified season.

        :param season_url: A URL of the season.
        :return: A filepath of the league.
        """
        *_, league_filename = season_url.split("/")
        league_filename = league_filename.replace("_", "-").lower()

        league_filepath = BaseConstants.RAW_FOLDER.joinpath(
            LeagueConstants.LEAGUES_FOLDER, league_filename
        )

        return league_filepath

    def get_leagues_html_data(self) -> None:
        """Get HTML pages (data) of the leagues for the seasons.

        :return: None.
        """
        seasons_urls = self.read_json(
            filepath=SeasonConstants.SEASONS_URLS_FILEPATH
        )

        for season, season_url in seasons_urls.items():
            league_html_data = self.get_html_data(url=season_url)
            league_filepath = self.get_league_filepath(season_url=season_url)

            self.save_html(
                html_data=league_html_data, filepath=league_filepath
            )
