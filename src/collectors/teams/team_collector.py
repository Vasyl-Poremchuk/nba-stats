from pathlib import Path

from collectors.base_collector import BaseCollector
from common.constants import BaseConstants, TeamConstants
from common.exceptions import HTMLExtensionError, SeasonYearError


class TeamCollector(BaseCollector):
    """A class to collect data for teams.

    :param encoding: The encoding of the data.
    """

    def __init__(self, encoding: str = "utf-8") -> None:
        """Construct all necessary attributes for the `TeamCollector`
        object.

        :param encoding: The encoding of the data.
        """
        super().__init__(encoding=encoding)

    def extract_filename(self, team_url: str) -> str:
        """Extract a team filename from the specified URL.

        Examples:

            - `https://.../teams/LAL/1998.html` -> `lal-1998.html`.
            - `https://.../teams/ATL/2023.html` -> `atl-2023.html`.

        :param team_url: A URL of the team.
        :raises SeasonYearError: If the season year is invalid.
        :raises HTMLExtensionError: If the URL doesn't end with an HTML
            extension.
        :return: A team filename.
        """
        *_, team, file_suffix = team_url.split("/")
        season_year, extension = file_suffix.split(".")

        if not self.is_season_year(season_year=season_year):
            raise SeasonYearError(year_txt=season_year)

        if extension != BaseConstants.RAW_FILE_EXTENSION:
            raise HTMLExtensionError(extension=extension)

        filename = f"{team.lower()}-{file_suffix}"

        return filename

    @staticmethod
    def get_team_filepath(filename: str) -> Path:
        """Get a filepath of the team based on the filename.

        :param filename: A filename of the team.
        :return: A filepath of the team.
        """
        team_filepath = BaseConstants.RAW_FOLDER.joinpath(
            TeamConstants.TEAMS_FOLDER, filename
        )

        return team_filepath

    def get_teams_html_data(self) -> None:
        """Get HTML pages (data) of the teams for the seasons.

        :return: None.
        """
        teams_urls = self.read_json(filepath=TeamConstants.RAW_FILEPATH)

        for season_year, urls in teams_urls.items():
            for team_url in urls:
                team_html_data = self.get_html_data(url=team_url)
                team_filename = self.extract_filename(team_url=team_url)
                team_filepath = self.get_team_filepath(filename=team_filename)

                self.save_html(
                    html_data=team_html_data, filepath=team_filepath
                )
