from datetime import datetime

import pytest

from extractors.players.player_stats_extractor import PlayerStatsExtractor


@pytest.mark.parametrize(
    "values, high_schools",
    [
        (
            [
                "MacDuffie School in Granby",
                "Massachusetts",
                "Redemption Christian Academy in Northfield",
                "Massachusetts",
            ],
            [
                "MacDuffie School in Granby, Massachusetts",
                "Redemption Christian Academy in Northfield, Massachusetts",
            ],
        ),
        (
            ["MacDuffie School in Granby", "Massachusetts"],
            ["MacDuffie School in Granby, Massachusetts"],
        ),
        ([], []),
    ],
)
def test_group_high_schools(
    player_stats_extractor: PlayerStatsExtractor,
    values: list[str],
    high_schools: list[str],
) -> None:
    """Test whether high schools are grouped by their locations.

    :param player_stats_extractor: An instance of the
        `PlayerStatsExtractor`.
    :param values: A list of values to group by.
    :param high_schools: A list of values to compare with the values
        returned from the method.
    :return: None.
    """
    assert player_stats_extractor.group_high_schools(values) == high_schools


@pytest.mark.parametrize(
    "value, idx, extracted_num_value",
    [
        ("1st round", 0, 1),
        ("46th overall", 0, 46),
        ("2021 NBA Draft", 0, 2021),
        ("", 0, None),
        ("2nd round (16th pick", 1, 16),
    ],
)
def test_extract_num_value(
    player_stats_extractor: PlayerStatsExtractor,
    value: str,
    idx: int,
    extracted_num_value: int,
) -> None:
    """Test whether an appropriate number is extracted.

    :param player_stats_extractor: An instance of the
        `PlayerStatsExtractor`.
    :param value: A value from which to extract.
    :param idx: An index of the value to extract.
    :param extracted_num_value: A value to compare with the value
        returned from the method.
    :return: None.
    """
    assert (
        player_stats_extractor.extract_num_value(value, idx=idx)
        == extracted_num_value
    )


@pytest.mark.parametrize(
    "values, keyword, draft_value",
    [
        (
            [
                "Toronto Raptors",
                "2nd round (16th pick",
                "46th overall)",
                "2021 NBA Draft",
            ],
            "round",
            "2nd round (16th pick",
        ),
        (
            [
                "Toronto Raptors",
                "2nd round (16th pick",
                "46th overall)",
                "2021 NBA Draft",
            ],
            "pick",
            "2nd round (16th pick",
        ),
        (
            [
                "Toronto Raptors",
                "2nd round (16th pick",
                "46th overall)",
                "2021 NBA Draft",
            ],
            "draft",
            "2021 NBA Draft",
        ),
        ([""], "draft", None),
        ([], "draft", None),
    ],
)
def test_get_draft_value(
    player_stats_extractor: PlayerStatsExtractor,
    values: list[str],
    keyword: str,
    draft_value: str,
) -> None:
    """Test whether an appropriate draft value is extracted.

    :param player_stats_extractor: An instance of the
        `PlayerStatsExtractor`.
    :param values: A list of values from which to extract.
    :param keyword: A keyword that should be in the desired value.
    :param draft_value: A value to compare with the value returned
        from the method.
    :return: None.
    """
    assert (
        player_stats_extractor.get_draft_value(values=values, keyword=keyword)
        == draft_value
    )


def test_extract_nba_debut(
    player_stats_extractor: PlayerStatsExtractor,
) -> None:
    """Test whether a string of the NBA debut is formatted correctly.

    :param player_stats_extractor: An instance of the
        `PlayerStatsExtractor`.
    :return: None.
    """
    assert (
        player_stats_extractor.extract_nba_debut("October 20, 2021")
        == datetime(2021, 10, 20).date()
    )


def test_extract_nba_debut_value_error(
    player_stats_extractor: PlayerStatsExtractor,
) -> None:
    """Test whether an appropriate error is raised if requirements
    aren't met.

    :param player_stats_extractor: An instance of the
        `PlayerStatsExtractor`.
    :return: None.
    """
    with pytest.raises(ValueError):
        player_stats_extractor.extract_nba_debut("20 October, 2021")
