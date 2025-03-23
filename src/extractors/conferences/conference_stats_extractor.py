import pandas as pd

from common.constants import (
    BaseConstants,
    ConferenceStatsConstants,
    LeagueConstants,
)
from extractors.base_extractor import BaseExtractor


class ConferenceStatsExtractor(BaseExtractor):
    """A class to extract data for conferences stats.

    :param header: An index of the table columns.
    """

    def __init__(self, header: int = 0) -> None:
        """Construct all attributes for the `ConferenceStatsExtractor`
        object.

        :param header: An index of the table columns.
        """
        super().__init__(header=header)

    @staticmethod
    def remove_empty_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Remove columns with empty data.

        :param df: A dataframe to remove empty columns.
        :return: Dataframe without empty columns.
        """
        temp_columns = df.columns

        for column in temp_columns:
            is_empty = df[column].isnull().all()

            if column.startswith("Unnamed:") and is_empty:
                df = df.drop(columns=column)

        return df

    def get_stats_df(
        self,
        stats_id: str,
        columns_map: dict[str, str],
        is_teams_stats: bool,
    ) -> pd.DataFrame:
        """Get a dataframe of stats.

        :param stats_id: Stats ID.
        :param columns_map: Map of column names.
        :param is_teams_stats: Whether the stats are teams stats.
        :return: Stats dataframe.
        """
        base_folder = BaseConstants.RAW_FOLDER.joinpath(
            LeagueConstants.LEAGUES_FOLDER
        )

        leagues_filepaths = self.get_filepaths(base_folder=base_folder)

        stats_dfs = []

        for league_filepath in leagues_filepaths:
            html_data = self.read_html(filepath=league_filepath)
            season, league = self.extract_season_league(
                filepath=league_filepath
            )

            season_year = self.get_season_year(season=season)

            header = self.header

            # Advanced and shooting stats have the first 2 rows as
            # columns. For them, we'll use the 2nd row as columns.
            if (
                stats_id == ConferenceStatsConstants.ADVANCED_STATS_TEAM_ID
                or stats_id.startswith("shooting-")
            ):
                header = (
                    ConferenceStatsConstants.ADVANCED_SHOOTING_STATS_HEADER
                )

            table_df = self.get_table_df_by_id(
                html_data=html_data,
                _id=stats_id,
                header=header,
            )

            # If the dataframe is empty, we'll skip it.
            if table_df.empty:
                continue

            # Remove columns that don't have values
            table_df = self.remove_empty_columns(df=table_df)

            table_df = self.rename_columns(
                table_df=table_df,
                columns_map=columns_map,
            )

            # At the end of each table we have the average stats for
            # all teams. We don't want to have that row and will filter
            # it out.
            table_df = table_df[table_df["rank"].notnull()]

            table_df["season"] = season
            table_df["league"] = league
            table_df["year"] = season_year

            table_df["is_playoff_team"] = table_df.apply(
                self.add_is_playoff_team, axis=1
            )
            table_df = self.remove_playoff_team_sign(df=table_df)

            table_df["is_team_stats"] = is_teams_stats

            stats_dfs.append(table_df)

        stats_df = pd.concat(stats_dfs)

        return stats_df

    def get_per_game_teams_stats_df(self) -> pd.DataFrame:
        """Get the per-game teams stats dataframe.

        :return: Teams stats dataframe.
        """
        per_game_teams_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.PER_GAME_STATS_TEAM_ID,
            columns_map=ConferenceStatsConstants.STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.TEAM_STATS,
        )

        per_game_teams_stats_df = per_game_teams_stats_df.astype(
            dtype=ConferenceStatsConstants.STATS_DATA_TYPES_MAP
        )

        return per_game_teams_stats_df

    def get_per_game_opponents_stats_df(self) -> pd.DataFrame:
        """Get the per-game opponents stats dataframe.

        :return: Opponents stats dataframe.
        """
        per_game_opponents_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.PER_GAME_STATS_OPPONENT_ID,
            columns_map=ConferenceStatsConstants.STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.OPPONENT_STATS,
        )

        per_game_opponents_stats_df = per_game_opponents_stats_df.astype(
            dtype=ConferenceStatsConstants.STATS_DATA_TYPES_MAP
        )

        return per_game_opponents_stats_df

    def get_total_teams_stats_df(self) -> pd.DataFrame:
        """Get the total teams stats dataframe.

        :return: Total teams stats dataframe.
        """
        total_teams_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.TOTAL_STATS_TEAM_ID,
            columns_map=ConferenceStatsConstants.STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.TEAM_STATS,
        )

        total_teams_stats_df = total_teams_stats_df.astype(
            dtype=ConferenceStatsConstants.STATS_DATA_TYPES_MAP
        )

        return total_teams_stats_df

    def get_total_opponents_stats_df(self) -> pd.DataFrame:
        """Get the total opponents stats dataframe.

        :return: Total opponents stats dataframe.
        """
        total_opponents_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.TOTAL_STATS_OPPONENT_ID,
            columns_map=ConferenceStatsConstants.STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.OPPONENT_STATS,
        )
        total_opponents_stats_df = total_opponents_stats_df.astype(
            dtype=ConferenceStatsConstants.STATS_DATA_TYPES_MAP
        )

        return total_opponents_stats_df

    def get_per_100_possessions_teams_stats_df(self) -> pd.DataFrame:
        """Get the per 100 possessions teams stats dataframe.

        :return: Per 100 possessions teams stats dataframe.
        """
        per_100_possessions_teams_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.PER_100_POSSESSIONS_STATS_TEAM_ID,
            columns_map=ConferenceStatsConstants.STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.TEAM_STATS,
        )

        per_100_possessions_teams_stats_df = (
            per_100_possessions_teams_stats_df.astype(
                dtype=ConferenceStatsConstants.STATS_DATA_TYPES_MAP
            )
        )

        return per_100_possessions_teams_stats_df

    def get_per_100_possessions_opponents_stats_df(self) -> pd.DataFrame:
        """Get the per 100 possessions opponents stats dataframe.

        :return: Per 100 possessions opponents stats dataframe.
        """
        per_100_possessions_opponents_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.PER_100_POSSESSIONS_STATS_OPPONENT_ID,
            columns_map=ConferenceStatsConstants.STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.OPPONENT_STATS,
        )

        per_100_possessions_opponents_stats_df = (
            per_100_possessions_opponents_stats_df.astype(
                dtype=ConferenceStatsConstants.STATS_DATA_TYPES_MAP
            )
        )

        return per_100_possessions_opponents_stats_df

    def get_advanced_teams_stats_df(self) -> pd.DataFrame:
        """Get the advanced teams stats dataframe.

        :return: Advanced teams stats dataframe.
        """
        advanced_teams_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.ADVANCED_STATS_TEAM_ID,
            columns_map=ConferenceStatsConstants.ADVANCED_STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.TEAM_STATS,
        )

        advanced_teams_stats_df = advanced_teams_stats_df.astype(
            dtype=ConferenceStatsConstants.ADVANCED_STATS_DATA_TYPES_MAP
        )

        return advanced_teams_stats_df

    def get_shooting_teams_stats_df(self) -> pd.DataFrame:
        """Get the shooting teams stats dataframe.

        :return: Shooting teams stats dataframe.
        """
        shooting_teams_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.SHOOTING_STATS_TEAM_ID,
            columns_map=ConferenceStatsConstants.SHOOTING_STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.TEAM_STATS,
        )

        shooting_teams_stats_df = shooting_teams_stats_df.astype(
            dtype=ConferenceStatsConstants.SHOOTING_STATS_DATA_TYPES_MAP
        )

        return shooting_teams_stats_df

    def get_shooting_opponents_stats_df(self) -> pd.DataFrame:
        """Get the shooting opponents stats dataframe.

        :return: Shooting opponents stats dataframe.
        """
        shooting_opponents_stats_df = self.get_stats_df(
            stats_id=ConferenceStatsConstants.SHOOTING_STATS_OPPONENT_ID,
            columns_map=ConferenceStatsConstants.SHOOTING_STATS_COLUMNS_MAP,
            is_teams_stats=ConferenceStatsConstants.OPPONENT_STATS,
        )

        shooting_opponents_stats_df = shooting_opponents_stats_df.astype(
            dtype=ConferenceStatsConstants.STATS_DATA_TYPES_MAP
        )

        return shooting_opponents_stats_df
