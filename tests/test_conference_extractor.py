import numpy as np
import pandas as pd
import pytest

from extractors.conferences.conference_extractor import ConferenceExtractor


@pytest.mark.parametrize(
    "row, division",
    [
        (pd.Series({"team": "Atlantic Division"}), "Atlantic"),
        (pd.Series({"team": "Boston Celtics"}), np.nan),
        (pd.Series({"team": ""}), np.nan),
        (pd.Series({"team": None}), np.nan),
    ],
)
def test_add_division(
    conference_extractor: ConferenceExtractor, row: pd.Series, division: str
) -> None:
    """Test whether a value in the dataframe is a division value.

    :param conference_extractor: An instance of the
        `ConferenceExtractor`.
    :param row: A row from which to extract a team.
    :param division: A value to compare with the value
        returned from the method.
    :return: None.
    """
    assert conference_extractor.add_division(row=row) == division or np.isnan(
        conference_extractor.add_division(row=row)
    )


@pytest.mark.parametrize(
    "df, modified_df",
    [
        (
            pd.DataFrame(
                [
                    {"team": "Atlantic Division"},
                    {"team": "Boston Celtics"},
                ],
                index=[0, 1],
            ),
            pd.DataFrame(
                [{"team": "Boston Celtics", "division": "Atlantic"}],
                index=[0],
            ),
        ),
        (
            pd.DataFrame(
                [
                    {"team": "Atlantic Division"},
                    {"team": "Boston Celtics"},
                    {"team": "Brooklyn Nets"},
                    {"team": "Central Division"},
                    {"team": "Indiana Pacers"},
                ],
                index=[0, 1, 2, 3, 4],
            ),
            pd.DataFrame(
                [
                    {"team": "Boston Celtics", "division": "Atlantic"},
                    {"team": "Brooklyn Nets", "division": "Atlantic"},
                    {"team": "Indiana Pacers", "division": "Central"},
                ],
                index=[0, 1, 2],
            ),
        ),
    ],
)
def test_add_divisions(
    conference_extractor: ConferenceExtractor,
    df: pd.DataFrame,
    modified_df: pd.DataFrame,
) -> None:
    """Test whether divisions are added correctly.

    :param conference_extractor: An instance of the
        `ConferenceExtractor`.
    :param df: A dataframe.
    :param modified_df: A dataframe to compare with the dataframe
        returned from the method.
    :return: None.
    """
    assert conference_extractor.add_divisions(df=df).equals(modified_df)


@pytest.mark.parametrize(
    "row, conference",
    [
        (pd.Series({"division": "Eastern"}), "Eastern"),
        (pd.Series({"division": "Western"}), "Western"),
        (pd.Series({"division": ""}), None),
        (pd.Series({"division": None}), None),
    ],
)
def test_add_conference(
    conference_extractor: ConferenceExtractor, row: pd.Series, conference: str
) -> None:
    """Test whether a conference is added correctly.

    :param conference_extractor: An instance of the
        `ConferenceExtractor`.
    :param row: A row from which to extract a division.
    :param conference: A value to compare with the value
        returned from the method.
    :return: None.
    """
    assert conference_extractor.add_conference(row=row) == conference
