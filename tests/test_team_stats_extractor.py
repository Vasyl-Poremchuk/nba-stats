import pytest

from extractors.teams.team_stats_extractor import TeamStatsExtractor


@pytest.mark.parametrize(
    "filename, team_year",
    [
        ("atl-1969.html", ("ATL", "1969")),
        ("dal-2003.html", ("DAL", "2003")),
    ],
)
def test_extract_team_year(
    team_stats_extractor: TeamStatsExtractor,
    filename: str,
    team_year: tuple[str, str],
) -> None:
    """Test whether team and year are correctly extracted.

    :param team_stats_extractor: An instance of the
        `TeamStatsExtractor`.
    :param filename: A filename from which to extract the team and year.
    :param team_year: A tuple of values to compare with the returned
        values from the method.
    :return: None.
    """
    assert (
        team_stats_extractor.extract_team_year(filename=filename) == team_year
    )
