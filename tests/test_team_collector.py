from pathlib import Path

import pytest

from collectors.teams.team_collector import TeamCollector
from common.constants import BaseConstants, TeamConstants
from common.exceptions import HTMLExtensionError, SeasonYearError


@pytest.mark.parametrize(
    "team_url, filename",
    [
        ("https://.../teams/LAL/1998.html", "lal-1998.html"),
        ("https://.../teams/ATL/2023.html", "atl-2023.html"),
    ],
)
def test_extract_filename(
    team_collector: TeamCollector, team_url: str, filename: str
) -> None:
    """Test whether a filename is properly extracted.

    :param team_collector: An instance of the `TeamCollector`.
    :param team_url: A team URL from which to extract the filename.
    :param filename: A filename to compare with the returned filename
        from the method.
    :return: None.
    """
    assert team_collector.extract_filename(team_url=team_url) == filename


@pytest.mark.parametrize(
    "team_url, error_msg",
    [
        (
            "https://.../teams/LAL/199.html",
            "Season year doesn't meet the requirements. Expected season year "
            "in format `YYYY`, got: `199`.",
        ),
        (
            "https://.../teams/ATL/2o23.html",
            "Season year doesn't meet the requirements. Expected season year "
            "in format `YYYY`, got: `2o23`.",
        ),
    ],
)
def test_extract_filename_season_year_error(
    team_collector: TeamCollector, team_url: str, error_msg: str
) -> None:
    """Test whether an appropriate error is raised if requirements
    aren't met.

    :param team_collector: An instance of the `TeamCollector`.
    :param team_url: A team URL from which to extract the filename.
    :param error_msg: An error message to compare with the returned
        message from the method.
    :return:
    """
    with pytest.raises(SeasonYearError, match=error_msg):
        team_collector.extract_filename(team_url=team_url)


@pytest.mark.parametrize(
    "team_url, error_msg",
    [
        (
            "https://.../teams/LAL/1993.htMl",
            "Unsupported file extension. Expected `html`, got: `htMl`.",
        ),
        (
            "https://.../teams/ATL/2023.csv",
            "Unsupported file extension. Expected `html`, got: `csv`.",
        ),
    ],
)
def test_extract_filename_html_extension_error(
    team_collector: TeamCollector, team_url: str, error_msg: str
) -> None:
    """Test whether an appropriate error is raised if requirements
    aren't met.

    :param team_collector: An instance of the `TeamCollector`.
    :param team_url: A team URL from which to extract the filename.
    :param error_msg: An error message to compare with the returned
        message from the method.
    :return: None.
    """
    with pytest.raises(HTMLExtensionError, match=error_msg):
        team_collector.extract_filename(team_url=team_url)


@pytest.mark.parametrize(
    "filename, team_filepath",
    [
        (
            "lal-1998.html",
            BaseConstants.RAW_FOLDER.joinpath(
                TeamConstants.TEAMS_FOLDER, "lal-1998.html"
            ),
        ),
        (
            "atl-2023.html",
            BaseConstants.RAW_FOLDER.joinpath(
                TeamConstants.TEAMS_FOLDER, "atl-2023.html"
            ),
        ),
    ],
)
def test_get_team_filepath(
    team_collector: TeamCollector, filename: str, team_filepath: Path
) -> None:
    """Test whether a method returns an appropriate constructed
    filepath.

    :param team_collector: An instance of the `TeamCollector`.
    :param filename: A filename.
    :param team_filepath: A filepath to compare with the returned
        filepath from the method.
    :return: None.
    """
    assert team_collector.get_team_filepath(filename=filename) == team_filepath
