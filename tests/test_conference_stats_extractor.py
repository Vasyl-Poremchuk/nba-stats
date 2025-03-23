import pandas as pd
import pytest

from extractors.conferences.conference_stats_extractor import (
    ConferenceStatsExtractor,
)


@pytest.mark.parametrize(
    "df, modified_df",
    [
        (
            pd.DataFrame({"team": "Boston Celtics"}, index=[0]),
            pd.DataFrame({"team": "Boston Celtics"}, index=[0]),
        ),
        (
            pd.DataFrame(
                [
                    {"team": "Boston Celtics", "Unnamed:": None},
                    {"team": "Chicago Bulls", "Unnamed:": None},
                ],
                index=[0, 1],
            ),
            pd.DataFrame(
                [{"team": "Boston Celtics"}, {"team": "Chicago Bulls"}],
                index=[0, 1],
            ),
        ),
    ],
)
def test_remove_empty_columns(
    conference_stats_extractor: ConferenceStatsExtractor,
    df: pd.DataFrame,
    modified_df: pd.DataFrame,
) -> None:
    """Test whether empty columns are removed.

    :param conference_stats_extractor: An instance of the
        `ConferenceStatsExtractor`.
    :param df: A dataframe.
    :param modified_df: A dataframe to compare with the dataframe
        returned from the method.
    :return: None.
    """
    assert conference_stats_extractor.remove_empty_columns(df=df).equals(
        modified_df
    )
