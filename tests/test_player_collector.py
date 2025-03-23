from pathlib import Path

import pytest

from collectors.players.player_collector import PlayerCollector
from common.constants import BaseConstants, PlayerConstants


@pytest.mark.parametrize(
    "player_url, player_filepath",
    [
        (
            "https://www.basketball-reference.com/players/b/barnedi01.html",
            BaseConstants.RAW_FOLDER.joinpath(
                PlayerConstants.PLAYERS_FOLDER, "barnedi01.html"
            ),
        ),
        (
            "https://www.basketball-reference.com/players/n/nelsodo01.html",
            BaseConstants.RAW_FOLDER.joinpath(
                PlayerConstants.PLAYERS_FOLDER, "nelsodo01.html"
            ),
        ),
    ],
)
def test_get_player_filepath(
    player_collector: PlayerCollector, player_url: str, player_filepath: Path
) -> None:
    """Test whether a method returns an appropriate filepath for the
    specified URL (source).

    :param player_collector: An instance of the `PlayerCollector`.
    :param player_url: A player URL.
    :param player_filepath: A filepath to compare with the filepath
        returned from the method.
    :return: None.
    """
    assert (
        player_collector.get_player_filepath(player_url=player_url)
        == player_filepath
    )
