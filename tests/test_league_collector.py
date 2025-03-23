from pathlib import Path

import pytest

from src.collectors.leagues.league_collector import LeagueCollector
from src.common.constants import BaseConstants, LeagueConstants


@pytest.mark.parametrize(
    "season_url, league_filepath",
    [
        (
            "https://www.basketball-reference.com/leagues/NBA_2024.html",
            BaseConstants.RAW_FOLDER.joinpath(
                LeagueConstants.LEAGUES_FOLDER, "nba-2024.html"
            ),
        ),
        (
            "https://www.basketball-reference.com/leagues/NBA_1956.html",
            BaseConstants.RAW_FOLDER.joinpath(
                LeagueConstants.LEAGUES_FOLDER, "nba-1956.html"
            ),
        ),
    ],
)
def test_get_league_filepath(
    league_collector: LeagueCollector, season_url: str, league_filepath: Path
) -> None:
    """Test whether a method returns an appropriate filepath for the
    specified URL (source).

    :param league_collector: An instance of the `LeagueCollector`.
    :param season_url: A season URL.
    :param league_filepath: A filepath to compare with the filepath
        returned from the method.
    :return: None.
    """
    assert (
        league_collector.get_league_filepath(season_url=season_url)
        == league_filepath
    )
