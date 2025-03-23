import pytest

from extractors.players.player_extractor import PlayerExtractor


@pytest.mark.parametrize(
    "player, is_true",
    [
        ("Walt Davis", True),
        ("...", False),
        ("123!", False),
        ("", False),
        ("   ", False),
        ("W@lt D@v1s", True),
    ],
)
def test_is_player(
    player_extractor: PlayerExtractor, player: str, is_true: bool
) -> None:
    """Test whether a player full name in appropriate format.

    :param player_extractor: An instance of the `PlayerExtractor`.
    :param player: A player full name to check.
    :param is_true: A logical value to compare with the returned
        value from the method.
    :return: None.
    """
    assert player_extractor.is_player(player=player) == is_true
