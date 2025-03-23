from pathlib import Path

import pandas as pd

from common.constants import BaseConstants, TeamConstants, TeamStatsConstants
from extractors.base_extractor import BaseExtractor


class TeamStatsExtractor(BaseExtractor):
    """A class to extract data for teams stats.

    :param header: An index of the table columns.
    """

    def __init__(self, header: int = 0) -> None:
        """Construct all attributes for the `TeamStatsExtractor` object.

        :param header: An index of the table columns.
        """
        super().__init__(header=header)

    @staticmethod
    def extract_team_year(filename: str) -> tuple[str, str]:
        """Extract a team and season year from the specified filename.

        Examples:

            - `atl-1969.html` -> (`ATL`, `1969`).
            - `dal-2003.html` -> (`DAL`, `2003`).

        :param filename: A filename from which to extract the team
            and year.
        :return: Team and season year.
        """
        values, _ = filename.split(".")
        team, season_year = values.split("-")

        return team.upper(), season_year

    def get_teams_filepaths(self) -> list[Path]:
        """Get filepaths of the teams.

        :return: Filepaths.
        """
        base_folder = BaseConstants.RAW_FOLDER.joinpath(
            TeamConstants.TEAMS_FOLDER
        )

        filepaths = self.get_filepaths(base_folder=base_folder)

        teams_filepaths = [
            team_filepath
            for team_filepath in filepaths
            if team_filepath.suffix == ".html"
        ]

        return teams_filepaths

    def get_stats_df(
        self,
        team_filepath: Path,
        *,
        stats_id: str,
        columns_map: dict[str, str]
    ) -> pd.DataFrame:
        """Get a dataframe of stats.

        :param team_filepath: Path to the team file.
        :param stats_id: Stats ID.
        :param columns_map: Map of column names.
        :return: Stats dataframe.
        """
        team_filename = team_filepath.name

        # Some of the tables we want to get from the HTML data are
        # in the comments. We need to remove them to get the data.
        html_data = (
            self.read_html(filepath=team_filepath)
            .replace("<!--", "")
            .replace("-->", "")
        )

        team, season_year = self.extract_team_year(filename=team_filename)
        season = self.get_season(year_txt=season_year)

        header = self.header

        # Adjusted shooting, shooting, and play-by-play stats have the
        # first 2 rows as columns. For them, we'll use the 2nd rows
        # as columns.
        if stats_id.startswith(
            (
                TeamStatsConstants.REGULAR_SEASON_ADJUSTED_SHOOTING_STATS_ID,
                TeamStatsConstants.REGULAR_SEASON_SHOOTING_STATS_ID,
                TeamStatsConstants.REGULAR_SEASON_PLAY_BY_PLAY_STATS_ID,
            )
        ):
            header = TeamStatsConstants.ADJUSTED_SHOOTING_STATS_HEADER

        stats_df = self.get_table_df_by_id(
            html_data=html_data,
            _id=stats_id,
            header=header,
        )

        stats_df = self.rename_columns(
            table_df=stats_df,
            columns_map=columns_map,
        )

        # At the end of each table we have the average stats for
        # all players. We don't want to have that row and will
        # filter it out. There is no `rank` column in the `roster`
        # table, so we'll ignore it.
        if "rank" in stats_df.columns:
            stats_df = stats_df[stats_df["rank"].notnull()]

        stats_df["team"] = team
        stats_df["season"] = season
        stats_df["year"] = season_year

        return stats_df

    def get_rosters_df(self) -> pd.DataFrame:
        """Get a rosters dataframe.

        :return: Roster dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        rosters_df = self.process_files(
            func=self.get_stats_df,
            filepaths=teams_filepaths,
            stats_id=TeamStatsConstants.ROSTER_ID,
            columns_map=TeamStatsConstants.ROSTER_COLUMNS_MAP,
        )

        rosters_df = rosters_df.astype(
            dtype=TeamStatsConstants.ROSTER_DATA_TYPES_MAP
        )

        return rosters_df

    def get_regular_season_per_game_stats_df(self) -> pd.DataFrame:
        """Get a regular season per game stats dataframe.

        :return: Per game stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_per_game_stats_df = self.process_files(
            func=self.get_stats_df,
            filepaths=teams_filepaths,
            stats_id=TeamStatsConstants.REGULAR_SEASON_PER_GAME_STATS_ID,
            columns_map=TeamStatsConstants.STATS_COLUMNS_MAP,
        )

        return regular_season_per_game_stats_df

    def get_playoffs_per_game_stats_df(self) -> pd.DataFrame:
        """Get a playoffs per game stats dataframe.

        :return: Per game stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_per_game_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_PER_GAME_STATS_ID,
            columns_map=TeamStatsConstants.STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_per_game_stats_df

    def get_regular_season_total_stats_df(self) -> pd.DataFrame:
        """Get a regular season total stats dataframe.

        :return: Total stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_total_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.REGULAR_SEASON_TOTAL_STATS_ID,
            columns_map=TeamStatsConstants.TOTAL_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return regular_season_total_stats_df

    def get_playoffs_total_stats_df(self) -> pd.DataFrame:
        """Get a playoffs total stats dataframe.

        :return: Total stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_total_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_TOTAL_STATS_ID,
            columns_map=TeamStatsConstants.TOTAL_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_total_stats_df

    def get_regular_season_per_36_minutes_stats_df(self) -> pd.DataFrame:
        """Get a regular season per 36 minutes stats dataframe.

        :return: Per 36 minutes stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_per_36_minutes_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.REGULAR_SEASON_PER_36_MINUTES_STATS_ID,
            columns_map=TeamStatsConstants.STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return regular_season_per_36_minutes_stats_df

    def get_playoffs_per_36_minutes_stats_df(self) -> pd.DataFrame:
        """Get a playoffs per 36 minutes stats dataframe.

        :return: Per 36 minutes stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_per_36_minutes_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_PER_36_MINUTES_STATS_ID,
            columns_map=TeamStatsConstants.STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_per_36_minutes_stats_df

    def get_regular_season_per_100_possessions_stats_df(self) -> pd.DataFrame:
        """Get a regular season per 100 possessions stats dataframe.

        :return: Per 100 possessions stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_per_100_possessions_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.REGULAR_SEASON_PER_100_POSSESSIONS_STATS_ID,
            columns_map=TeamStatsConstants.PER_100_POSSESSIONS_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return regular_season_per_100_possessions_stats_df

    def get_playoffs_per_100_possessions_stats_df(self) -> pd.DataFrame:
        """Get a playoffs per 100 possessions stats dataframe.

        :return: Per 100 possessions stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_per_100_possessions_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_PER_100_POSSESSIONS_STATS_ID,
            columns_map=TeamStatsConstants.PER_100_POSSESSIONS_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_per_100_possessions_stats_df

    def get_regular_season_advanced_stats_df(self) -> pd.DataFrame:
        """Get a regular season advanced stats dataframe.

        :return: Advanced stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_advanced_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.REGULAR_SEASON_ADVANCED_STATS_ID,
            columns_map=TeamStatsConstants.ADVANCED_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return regular_season_advanced_stats_df

    def get_playoffs_advanced_stats_df(self) -> pd.DataFrame:
        """Get a playoffs advanced stats dataframe.

        :return: Advanced stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_advanced_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_ADVANCED_STATS_ID,
            columns_map=TeamStatsConstants.ADVANCED_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_advanced_stats_df

    def get_regular_season_adjusted_shooting_stats_df(self) -> pd.DataFrame:
        """Get a regular season adjusted shooting stats dataframe.

        :return: Adjusted shooting stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_adjusted_shooting_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.REGULAR_SEASON_ADJUSTED_SHOOTING_STATS_ID,
            columns_map=TeamStatsConstants.ADJUSTED_SHOOTING_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return regular_season_adjusted_shooting_stats_df

    def get_playoffs_adjusted_shooting_stats_df(self) -> pd.DataFrame:
        """Get a playoffs adjusted shooting stats dataframe.

        :return: Adjusted shooting stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_adjusted_shooting_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_ADJUSTED_SHOOTING_STATS_ID,
            columns_map=TeamStatsConstants.ADJUSTED_SHOOTING_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_adjusted_shooting_stats_df

    def get_regular_season_shooting_stats_df(self) -> pd.DataFrame:
        """Get a regular season shooting stats dataframe.

        :return: Shooting stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_shooting_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.REGULAR_SEASON_SHOOTING_STATS_ID,
            columns_map=TeamStatsConstants.SHOOTING_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return regular_season_shooting_stats_df

    def get_playoffs_shooting_stats_df(self) -> pd.DataFrame:
        """Get a playoffs shooting stats dataframe.

        :return: Shooting stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_season_shooing_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_SHOOTING_STATS_ID,
            columns_map=TeamStatsConstants.SHOOTING_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_season_shooing_stats_df

    def get_regular_season_play_by_play_stats_df(self) -> pd.DataFrame:
        """Get a regular season play-by-play stats dataframe.

        :return: Play-by-play stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        regular_season_play_by_play_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.REGULAR_SEASON_PLAY_BY_PLAY_STATS_ID,
            columns_map=TeamStatsConstants.PLAY_BY_PLAY_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return regular_season_play_by_play_stats_df

    def get_playoffs_play_by_play_stats_df(self) -> pd.DataFrame:
        """Get a playoffs play-by-play stats dataframe.

        :return: Play-by-play stats dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        playoffs_season_play_by_play_stats_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.PLAYOFFS_PLAY_BY_PLAY_STATS_ID,
            columns_map=TeamStatsConstants.PLAY_BY_PLAY_STATS_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return playoffs_season_play_by_play_stats_df

    def get_salaries_df(self) -> pd.DataFrame:
        """Get a salaries dataframe.

        :return: Salaries dataframe.
        """
        teams_filepaths = self.get_teams_filepaths()

        salaries_df = self.process_files(
            func=self.get_stats_df,
            stats_id=TeamStatsConstants.SALARIES_ID,
            columns_map=TeamStatsConstants.SALARIES_COLUMNS_MAP,
            filepaths=teams_filepaths,
        )

        return salaries_df
