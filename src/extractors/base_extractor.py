import concurrent.futures
import io
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Callable

import bs4
import pandas as pd
from pandas import Series

from common.constants import BaseConstants
from common.exceptions import FileProcessingError


class BaseExtractor:
    """A base class to use for data extractors.

    :param header: An index of the table columns.
    """

    def __init__(self, header: int = None) -> None:
        """Construct all attributes for the `BaseExtractor` object.

        :param header: An index of the table columns.
        """
        self.header = header

    @staticmethod
    def read_html(filepath: Path) -> str:
        """Read an HTML data from the specified filepath.

        :param filepath: Filepath to save the HTML data to.
        :return: HTML data.
        """
        with open(filepath, mode="r", encoding="utf-8") as f:
            html_data = f.read()

        return html_data

    @staticmethod
    def get_soup(html_data: str) -> bs4.BeautifulSoup:
        """Get a BeautifulSoup object from the HTML data.

        :param html_data: HTML data.
        :return: A BeautifulSoup object.
        """
        soup = bs4.BeautifulSoup(html_data, features="lxml")

        return soup

    def get_table(self, *, filepath: Path, index: int) -> pd.DataFrame:
        """Get a table of from the specified source (URL).

        :param filepath: Filepath of the file.
        :param index: Index of the table.
        :return: A table as a dataframe.
        """
        table = pd.read_html(filepath, header=self.header, encoding="utf-8")[
            index
        ]

        return table

    @staticmethod
    def rename_columns(
        table_df: pd.DataFrame, *, columns_map: dict[str, str]
    ) -> pd.DataFrame:
        """Rename columns of the specified table.

        :param table_df: A table to rename columns.
        :param columns_map: Columns to rename.
        :return: A table with renamed columns.
        """
        table_df = table_df.rename(columns=columns_map)

        return table_df

    @staticmethod
    def save_table(table_df: pd.DataFrame, *, filepath: Path) -> None:
        """Save a table to the specified filepath.

        :param table_df: A table to save.
        :param filepath: A filepath to save the table to.
        :return: None.
        """
        table_df.to_parquet(
            filepath, engine="pyarrow", compression="snappy", index=False
        )

    @staticmethod
    def save_json(json_data: dict, *, filepath: Path) -> None:
        """Save JSON data to the specified filepath.

        :param json_data: dict: JSON data.
        :param filepath: Filepath to save the JSON data.
        :return: None.
        """
        with open(filepath, mode="w", encoding="utf-8") as f:
            json.dump(json_data, f)

    @staticmethod
    def make_base_folder(base_path: Path, folder: str) -> None:
        """Create the base folder.

        :param base_path: Base path in which to create the folder.
        :param folder: Folder to create.
        :return: None.
        """
        base_folder = base_path.joinpath(folder)

        os.makedirs(base_folder, exist_ok=True)

    @staticmethod
    def get_season(year_txt: str) -> str:
        """Get the season from the specified text.

        :param year_txt: A string representing the year.
        :return: Season
        """
        year = datetime.strptime(year_txt, "%Y").year

        season = f"{year - 1}-{year % 100:02d}"

        return season

    def extract_season_league(self, filepath: Path) -> tuple[str, str]:
        """Extract the season and league from the file.

        :param filepath: Filepath to extract season/league from.
        :return: Season and league.
        """
        filename = filepath.name
        league, year_txt = filename.replace(".html", "").split("-")

        season = self.get_season(year_txt=year_txt)

        season_league = (season, league.upper())

        return season_league

    @staticmethod
    def get_season_year(season: str) -> int:
        """Get a year from the specified season.

        :param season: Season to extract from.
        :return: Year of the season.
        """
        year, _ = season.split("-")

        season_year = int(year) + 1

        return season_year

    @staticmethod
    def add_is_playoff_team(row: Series) -> bool:
        """Add a boolean value that indicates if the team was in
        playoffs. If the team name ends with `*`, the team was in
        playoffs, otherwise not.

        :param row: Row to add a value to.
        :return: Whether the team was in the playoffs or not.
        """
        team = row["team"]

        if team.endswith("*"):
            return True

        return False

    @staticmethod
    def remove_playoff_team_sign(df: pd.DataFrame) -> pd.DataFrame:
        """Remove the playoff team sign (`*`) from a column (`team`) of
        the dataframe.

        :param df: Dataframe to remove the playoff team sign from.
        :return: Dataframe without the playoff team sign removed.
        """
        df["team"] = df["team"].str.replace("*", "")

        return df

    @staticmethod
    def get_filepaths(base_folder: Path) -> list[Path]:
        """Get all files in the specified folder.

        :param base_folder: Base folder.
        :return: Filepaths.
        """
        filepaths = [
            base_folder.joinpath(filename)
            for filename in os.listdir(base_folder)
        ]

        return filepaths

    def get_table_df_by_id(
        self, html_data: str, *, _id: str, header: int
    ) -> pd.DataFrame:
        """Get a table by its tag ID as a dataframe.

        :param html_data: HTML data.
        :param _id: An ID of the table.
        :param header: An index of the table headers.
        :return: A table of stats.
        """
        soup = self.get_soup(html_data=html_data)
        selector = f"table[id='{_id}']"

        table = soup.select_one(selector=selector)

        # Some seasons don't have certain stats.
        # In this case, we'll return an emtpy dataframe.
        if not table:
            return pd.DataFrame()

        io_table = io.StringIO(str(table))

        table_df = pd.read_html(io_table, header=header, encoding="utf-8")[0]

        return table_df

    @staticmethod
    def process_files(
        func: Callable, filepaths: list[Path], **kwargs
    ) -> pd.DataFrame:
        """Process a list of filepaths.

        :param func: A function to extract data from HTML data.
        :param filepaths: Filepaths of stats.
        :raises FileProcessingError: If file processing fails.
        :return: Concatenated dataframe.
        """
        dfs = []

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=BaseConstants.MAX_WORKERS
        ) as executor:
            futures = {}

            for filepath in filepaths:
                future = executor.submit(func, filepath, **kwargs)

                futures[future] = filepath

            for future in concurrent.futures.as_completed(futures):
                filepath = futures.get(future)

                try:
                    df = future.result()

                    dfs.append(df)
                except Exception as e:
                    raise FileProcessingError(filename=filepath.name, e=e)

        concat_df = pd.concat(dfs)

        return concat_df
