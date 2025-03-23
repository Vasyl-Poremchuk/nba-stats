from pathlib import Path

import numpy as np
import pandas as pd

from common.constants import (
    BaseConstants,
    ConferenceConstants,
    LeagueConstants,
)
from extractors.base_extractor import BaseExtractor


class ConferenceExtractor(BaseExtractor):
    """A class to extract data for conferences.

    :param header: An index of the table columns.
    """

    EASTERN_CONFERENCE = "Eastern"
    WESTERN_CONFERENCE = "Western"

    def __init__(self, header: int = 0) -> None:
        """Construct all attributes for the `ConferenceExtractor`
        object.

        :param header: An index of the table columns.
        """
        super().__init__(header=header)

    @staticmethod
    def add_division(row: pd.Series) -> str | float:
        """Add a division to the given row.

        :param row: A row to add division to.
        :return: Division name.
        """
        team = row["team"]

        if isinstance(team, str) and team.endswith(" Division"):
            division, _ = team.split(" ")

            return division

        return np.nan

    def add_divisions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add divisions to the specified dataframe.

        :param df: A dataframe to add divisions to.
        :return: Dataframe with divisions added.
        """
        df["division"] = df.apply(self.add_division, axis=1)

        df["division"] = df["division"].ffill()

        df = df[~df["team"].str.endswith(" Division")].reset_index(drop=True)

        return df

    def get_conference_df_ge_1971(
        self,
        filepath: Path,
        *,
        eastern_index: int,
        western_index: int,
        season: str,
        league: str,
        year: int,
    ) -> pd.DataFrame:
        """Get a conference dataframe of a season where the year in
        a range [1971, 2024].

        :param filepath: A filepath to extract a conference from.
        :param eastern_index: An index of eastern conference.
        :param western_index: An index of western conference.
        :param season: A season to add as a column value.
        :param league: A league to add as a column value.
        :param year: A year to add as a column value.
        :return: Conference dataframe.
        """
        eastern_conference_df = self.get_table(
            filepath=filepath, index=eastern_index
        )
        western_conference_df = self.get_table(
            filepath=filepath, index=western_index
        )

        eastern_conference_df = self.rename_columns(
            table_df=eastern_conference_df,
            columns_map=ConferenceConstants.COLUMNS_MAP,
        )
        western_conference_df = self.rename_columns(
            table_df=western_conference_df,
            columns_map=ConferenceConstants.COLUMNS_MAP,
        )

        eastern_conference_df["conference"] = (
            ConferenceExtractor.EASTERN_CONFERENCE
        )
        western_conference_df["conference"] = (
            ConferenceExtractor.WESTERN_CONFERENCE
        )

        eastern_conference_df = self.add_divisions(df=eastern_conference_df)
        western_conference_df = self.add_divisions(df=western_conference_df)

        conference_df = pd.concat(
            [eastern_conference_df, western_conference_df]
        )

        conference_df["season"] = season
        conference_df["league"] = league
        conference_df["year"] = year

        return conference_df

    @staticmethod
    def add_conference(row: pd.Series) -> str | None:
        """Add a conference to the given row.

        :param row: A row to add conference to.
        :return: Conference name.
        """
        division = row["division"]

        if division == ConferenceExtractor.EASTERN_CONFERENCE:
            return ConferenceExtractor.EASTERN_CONFERENCE

        if division == ConferenceExtractor.WESTERN_CONFERENCE:
            return ConferenceExtractor.WESTERN_CONFERENCE

    def get_conference_df_ge_1956(
        self, filepath: Path, *, season: str, league: str, year: int
    ) -> pd.DataFrame:
        """Get a conference dataframe of a season where the year in
        a range [1956, 1970].

        :param filepath: A filepath to extract a conference from.
        :param season: A season to add as a column value.
        :param league: A league to add as a column value.
        :param year: A year to add as a column value.
        :return: Conference dataframe.
        """
        conference_df = self.get_table(filepath=filepath, index=0)

        conference_df = self.rename_columns(
            table_df=conference_df, columns_map=ConferenceConstants.COLUMNS_MAP
        )

        conference_df = self.add_divisions(df=conference_df)
        conference_df["conference"] = conference_df.apply(
            self.add_conference, axis=1
        )
        conference_df["season"] = season
        conference_df["league"] = league
        conference_df["year"] = year

        return conference_df

    def get_conferences_df(self) -> pd.DataFrame:
        """Get a dataframe of all conferences.

        :return: Conferences dataframe.
        """
        base_folder = BaseConstants.RAW_FOLDER.joinpath(
            LeagueConstants.LEAGUES_FOLDER
        )

        leagues_filepaths = self.get_filepaths(base_folder=base_folder)

        conferences_dfs = []

        for league_filepath in leagues_filepaths:
            season, league = self.extract_season_league(
                filepath=league_filepath
            )

            season_year = self.get_season_year(season=season)

            if season_year >= 2016:
                conference_df = self.get_conference_df_ge_1971(
                    filepath=league_filepath,
                    eastern_index=2,
                    western_index=3,
                    season=season,
                    league=league,
                    year=season_year,
                )

                conferences_dfs.append(conference_df)
            elif season_year >= 1971:
                conference_df = self.get_conference_df_ge_1971(
                    filepath=league_filepath,
                    eastern_index=0,
                    western_index=1,
                    season=season,
                    league=league,
                    year=season_year,
                )

                conferences_dfs.append(conference_df)
            elif season_year >= 1956:
                conference_df = self.get_conference_df_ge_1956(
                    filepath=league_filepath,
                    season=season,
                    league=league,
                    year=season_year,
                )

                conferences_dfs.append(conference_df)

        conferences_df = pd.concat(conferences_dfs)

        return conferences_df

    def update_conferences_df(self) -> pd.DataFrame:
        """Update data types and add other column values for the
        specified dataframe.

        :return: Updated conferences dataframe.
        """
        conferences_df = self.get_conferences_df()

        conferences_df["is_playoff_team"] = conferences_df.apply(
            self.add_is_playoff_team, axis=1
        )

        conferences_df = self.remove_playoff_team_sign(df=conferences_df)
        conferences_df["games_behind"] = conferences_df[
            "games_behind"
        ].str.replace("—", "0")

        conferences_df = conferences_df.astype(
            dtype=ConferenceConstants.DATA_TYPES_MAP
        )
        conferences_df["games_behind"] = conferences_df["games_behind"].astype(
            dtype=int
        )

        return conferences_df
