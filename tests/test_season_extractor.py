import pytest

from common.exceptions import SeasonYearError
from extractors.seasons.season_extractor import SeasonExtractor


def test_extract_season(season_extractor: SeasonExtractor) -> None:
    """Test whether a season is formatted correctly.

    :param season_extractor: An instance of the `SeasonExtractor`.
    :return: None.
    """
    assert (
        season_extractor.extract_season(href="/leagues/NBA_2024.html")
        == "2023-24"
    )


@pytest.mark.parametrize(
    "href, error_msg",
    [
        (
            "/leagues/NBA_2o24.html",
            "Season year doesn't meet the requirements. Expected season year "
            "in format `YYYY`, got: `2o24`.",
        ),
        (
            "/leagues/NBA_aaaa.html",
            "Season year doesn't meet the requirements. Expected season year "
            "in format `YYYY`, got: `aaaa`.",
        ),
        (
            "/leagues/NBA_193.html",
            "Season year doesn't meet the requirements. Expected season year "
            "in format `YYYY`, got: `193`.",
        ),
    ],
)
def test_extract_season_year_error(
    season_extractor: SeasonExtractor, href: str, error_msg: str
) -> None:
    """Test whether an appropriate error is raised if requirements
    aren't met.

    :param season_extractor: An instance of the `SeasonExtractor`.
    :param href: A href value from which to extract the season year.
    :param error_msg: An error message to compare with the returned
        message from the method.
    :return: None.
    """
    with pytest.raises(SeasonYearError, match=error_msg):
        season_extractor.extract_season(href=href)
