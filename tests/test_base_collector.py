from unittest.mock import MagicMock, patch

import pytest

from collectors.base_collector import BaseCollector


def test_get_html_data(base_collector: BaseCollector) -> None:
    """Test the retrieval of HTML data from the specified URL (source).

    :param base_collector: An instance of the `BaseCollector`.
    :return: None.
    """
    mock_html_data = MagicMock()
    mock_html_data.content.decode.return_value = (
        "<html><body><h1>NBA</h1></body></html>"
    )
    mock_html_data.status_code = 200

    with patch(
        "collectors.base_collector.requests.get", return_value=mock_html_data
    ) as mock_get:
        html_data = base_collector.get_html_data(
            url="https://www.basketball-reference.com/leagues/NBA_2024.html"
        )

        assert html_data == "<html><body><h1>NBA</h1></body></html>"
        mock_get.assert_called_once_with(
            url="https://www.basketball-reference.com/leagues/NBA_2024.html"
        )


@pytest.mark.parametrize(
    "season_year, is_true",
    [("2o24", False), ("193", False), ("aaaa", False), ("2024", True)],
)
def test_is_season_year(
    base_collector: BaseCollector, season_year: str, is_true: bool
) -> None:
    """Test whether the specified season year is the actual year.

    :param base_collector: An instance of the `BaseCollector`.
    :param season_year: A season year to test.
    :param is_true: A logical value to compare with the value
        returned from the method.
    :return: None.
    """
    assert base_collector.is_season_year(season_year=season_year) == is_true
