import re

import pandas as pd

from common.constants import BaseConstants, SeasonConstants
from common.exceptions import SeasonYearError
from extractors.base_extractor import BaseExtractor


class SeasonExtractor(BaseExtractor):
    """A class to extract data for seasons.

    :param header: An index of the table columns.
    :param index: An index of the table to extract data from.
    """

    def __init__(self, header: int = 1, index: int = 0) -> None:
        """Construct all attributes for the `SeasonExtractor` object.

        :param header: An index of the table columns.
        :param index: An index of the table to extract data from.
        """
        super().__init__(header=header)
        self.index = index

    def get_seasons_df(self) -> pd.DataFrame:
        """Get a dataframe of all seasons.

        :return: Seasons dataframe.
        """
        seasons_df = self.get_table(
            filepath=SeasonConstants.RAW_FILEPATH, index=self.index
        )

        seasons_df = self.rename_columns(
            table_df=seasons_df, columns_map=SeasonConstants.COLUMNS_MAP
        )

        # We need to filter seasons for the following columns as they
        # might be empty.
        seasons_df = seasons_df[
            (seasons_df["league"] == SeasonConstants.LEAGUE_TO_SELECT)
            & (seasons_df["champion"].notnull())
            & (seasons_df["mvp"].notnull())
            & (seasons_df["rookie_of_the_year"].notnull())
        ]

        return seasons_df

    def get_filtered_seasons(self) -> list[str]:
        """Get a list of filtered seasons (that meets requirements).

        The following requirements were used:

            - The league is `NBA`.
            - Values in the `champion` column aren't empty.
            - Values in the `mvp` column aren't empty.
            - Values in the `rookie_of_the_year` column aren't empty.

        NOTE: The `seasons_df` already meets the requirements.

        :return: Filtered seasons.
        """
        seasons_df = self.get_seasons_df()

        filtered_seasons = seasons_df["season"].to_list()

        return filtered_seasons

    def extract_season(self, *, href: str) -> str:
        """Extract a season from the specified href value.

        :param href: Season href.
        :return: Season.
        """
        *_, filename = href.split("/")
        _, year_txt = filename.replace(".html", "").split("_")

        try:
            season = self.get_season(year_txt=year_txt)

            return season
        except ValueError:
            raise SeasonYearError(year_txt=year_txt)

    def get_seasons_urls(self) -> dict[str, str]:
        """Get URLs of all seasons.

        :return: URLs.
        """
        html_data = self.read_html(filepath=SeasonConstants.RAW_FILEPATH)
        soup = self.get_soup(html_data=html_data)

        filtered_seasons = self.get_filtered_seasons()

        pattern = re.compile(pattern=SeasonConstants.SEASON_HREF_PATTERN)

        tags = soup.find_all(name="a", attrs={"href": pattern})

        seasons_urls = {}

        for tag in tags:
            href = tag.attrs.get("href")
            season = self.extract_season(href=href)

            if season in filtered_seasons:
                seasons_urls[season] = BaseConstants.URL + href

        return seasons_urls
