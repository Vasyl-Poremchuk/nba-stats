import bs4

from common.constants import BaseConstants, TeamConstants, LeagueConstants
from extractors.base_extractor import BaseExtractor


class TeamExtractor(BaseExtractor):
    """A class to extract data for teams.

    :param header: An index of the table columns.
    :param index: An index of the table to extract data from.
    """

    def __init__(self, header: int = 1, index: int = 0) -> None:
        """Construct all attributes for the `TeamExtractor` object.

        :param header: An index of the table columns.
        :param index: An index of the table to extract data from.
        """
        super().__init__(header=header)
        self.index = index

    @staticmethod
    def get_season_teams_urls(soup: bs4.BeautifulSoup, *, selector: str):
        """Get URLs of the teams from the current season data
        (HTML page).

        :param soup: Soup object of the HTML page.
        :param selector: CSS selector of the search value.
        :return: URLs of the teams.
        """
        season_teams_urls = [
            BaseConstants.URL + href.attrs.get("href")
            for href in soup.select(selector=selector)
        ]

        return season_teams_urls

    def get_teams_urls(self) -> dict[int, list[str]]:
        """Get URLs of the teams from all seasons.

        :return: URLs.
        """
        base_folder = BaseConstants.RAW_FOLDER.joinpath(
            LeagueConstants.LEAGUES_FOLDER
        )

        filepaths = self.get_filepaths(base_folder=base_folder)

        teams_urls = {}

        for filepath in filepaths:
            season, _ = self.extract_season_league(filepath=filepath)
            season_year = self.get_season_year(season=season)

            html_data = self.read_html(filepath=filepath)
            soup = self.get_soup(html_data=html_data)

            season_teams_urls = self.get_season_teams_urls(
                soup=soup, selector=TeamConstants.TEAM_HREF_SELECTOR
            )

            teams_urls[season_year] = season_teams_urls

        return teams_urls
