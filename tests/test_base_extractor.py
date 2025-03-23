from pathlib import Path

import pandas as pd
import pytest

from common.constants import BaseConstants, LeagueConstants
from extractors.base_extractor import BaseExtractor


@pytest.mark.parametrize(
    "table_df, columns_map",
    [
        (
            pd.DataFrame(
                data={"Team": "Boston Celtics", "W": 64, "L": 3}, index=[0]
            ),
            {"Team": "team", "W": "wins", "L": "loses"},
        ),
        (
            pd.DataFrame(
                data=[
                    {"Team": "Boston Celtics", "W": 64, "L": 6},
                    {"Team": "Atlanta Hawks", "W": 55, "L": 15},
                ],
                index=[0, 1],
            ),
            {"Team": "team", "W": "wins", "L": "loses"},
        ),
    ],
)
def test_rename_columns(
    base_extractor: BaseExtractor,
    table_df: pd.DataFrame,
    columns_map: dict[str, str],
) -> None:
    """Test whether the columns of the dataframe are renamed.

    :param base_extractor: An instance of the `BaseExtractor`.
    :param table_df: A table dataframe.
    :param columns_map: A list of columns to use.
    :return: None.
    """
    df = base_extractor.rename_columns(
        table_df=table_df, columns_map=columns_map
    )

    assert list(df.columns) == list(columns_map.values())


@pytest.mark.parametrize(
    "year_txt, season", [("2024", "2023-24"), ("1956", "1955-56")]
)
def test_get_season(
    base_extractor: BaseExtractor, year_txt: str, season: str
) -> None:
    """Test whether the specified season is formatted correctly.

    :param base_extractor: An instance of the `BaseExtractor`.
    :param year_txt: A string from which to extract the season year.
    :param season: A value to compare with the value
        returned from the method.
    :return: None.
    """
    assert base_extractor.get_season(year_txt=year_txt) == season


@pytest.mark.parametrize(
    "filepath, season_league",
    [
        (
            BaseConstants.RAW_FOLDER.joinpath(
                LeagueConstants.LEAGUES_FOLDER, "nba-1962.html"
            ),
            ("1961-62", "NBA"),
        ),
        (
            BaseConstants.RAW_FOLDER.joinpath(
                LeagueConstants.LEAGUES_FOLDER, "nba-2024.html"
            ),
            ("2023-24", "NBA"),
        ),
    ],
)
def test_extract_season_league(
    base_extractor: BaseExtractor, filepath: Path, season_league: str
) -> None:
    """Test whether the season year and league are extracted correctly.

    :param base_extractor: An instance of the `BaseExtractor`.
    :param filepath: A filepath from which to extract the season year
        and league.
    :param season_league: Season year and league to compare with the
        value returned from the method.
    :return: None.
    """
    assert (
        base_extractor.extract_season_league(filepath=filepath)
        == season_league
    )


@pytest.mark.parametrize(
    "season, season_year",
    [
        ("1972-73", 1973),
        ("2023-24", 2024),
    ],
)
def test_get_season_year(
    base_extractor: BaseExtractor, season: str, season_year: int
) -> None:
    """Test whether the year is extracted correctly from the specified
    season year.

    :param base_extractor: An instance of the `BaseExtractor`.
    :param season: A season year from which to extract the year.
    :param season_year: A value to compare with the value
        returned from the method.
    :return: None.
    """
    assert base_extractor.get_season_year(season=season) == season_year


@pytest.mark.parametrize(
    "row, is_playoff_team",
    [
        (pd.Series({"team": ""}), False),
        (pd.Series({"team": "Toronto Raptors"}), False),
        (pd.Series({"team": "Boston Celtics*"}), True),
    ],
)
def test_add_is_playoff_team(
    base_extractor: BaseExtractor, row: pd.Series, is_playoff_team: bool
) -> None:
    """Test whether a logical indicator is added correctly for playoff
    teams.

    :param base_extractor: An instance of the `BaseExtractor`.
    :param row: A row from which to extract the team.
    :param is_playoff_team: A logical value to compare with the value
        returned from the method.
    :return: None.
    """
    assert base_extractor.add_is_playoff_team(row=row) == is_playoff_team


@pytest.mark.parametrize(
    "df, processed_df",
    [
        (
            pd.DataFrame({"team": ""}, index=[0]),
            pd.DataFrame({"team": ""}, index=[0]),
        ),
        (
            pd.DataFrame({"team": "Toronto Raptors"}, index=[0]),
            pd.DataFrame({"team": "Toronto Raptors"}, index=[0]),
        ),
        (
            pd.DataFrame({"team": "Boston Celtics*"}, index=[0]),
            pd.DataFrame({"team": "Boston Celtics"}, index=[0]),
        ),
    ],
)
def test_remove_playoff_team_sign(
    base_extractor: BaseExtractor, df: pd.DataFrame, processed_df: pd.DataFrame
) -> None:
    """Test whether a playoff team sign is removed correctly for playoff
    teams.

    :param base_extractor: An instance of the `BaseExtractor`.
    :param df: A dataframe.
    :param processed_df: A dataframe to compare with the dataframe
        returned from the method.
    :return: None.
    """
    assert base_extractor.remove_playoff_team_sign(df=df).equals(processed_df)
