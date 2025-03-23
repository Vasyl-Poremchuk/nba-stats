import json
import logging
import os
import re
import time
from pathlib import Path

import requests

from common.constants import BaseConstants, LoggerConstants, SeasonConstants
from common.logger import init_logger

init_logger(logger_name=LoggerConstants.BASE_COLLECTOR_LOGGER_NAME)
logger = logging.getLogger(name=LoggerConstants.BASE_COLLECTOR_LOGGER_NAME)


class BaseCollector:
    """A base class to use for data collectors.

    :param encoding: The encoding of the data.
    """

    def __init__(self, encoding: str = "utf-8") -> None:
        """Construct all necessary attributes for the `BaseCollector`
        object.

        :param encoding: The encoding of the data.
        """
        self.encoding = encoding

    def get_html_data(self, url: str) -> str | None:
        """Get an HTML data as a response from the specified source.

        :param url: A URL of the HTML data.
        :return: HTML data.
        """
        try:
            response = requests.get(url=url)
            response.raise_for_status()

            # Don't use the `response.text` as it doesn't properly
            # convert some special characters. For example, we want
            # to get this: `N. Jokić` instead we get: `N. JokiÄ`.
            html_data = response.content.decode(self.encoding)

            # We need to specify a delay between the next response,
            # otherwise we'll be blocked.
            time.sleep(BaseConstants.TIME_SLEEP_SECONDS)

            return html_data
        except requests.exceptions.RequestException as e:
            status_code = e.response.status_code

            match status_code:
                case 400:
                    logger.error(
                        msg=f"HTML data can't be retrieved due to "
                        f"`{status_code}` Bad Request for `{url}`.",
                    )
                case 401 | 403:
                    logger.error(
                        f"HTML data can't be retrieved due to `{status_code}` "
                        f"Authentication Error for `{url}`."
                    )
                case 404:
                    logger.error(
                        f"HTML data isn't available due to `{status_code}` "
                        f"Not Found for `{url}`."
                    )
                case _:
                    logger.error(
                        f"An unexpected error occurred while fetching HTML "
                        f"data due to `{e}` for `{url}`."
                    )

    def save_html(self, html_data: str, *, filepath: Path) -> None:
        """Save HTML data to the appropriate filepath.

        :param html_data: HTML data from the response.
        :param filepath: A filepath to save the HTML data to.
        :return: None.
        """
        with open(filepath, mode="w", encoding=self.encoding) as f:
            f.write(html_data)

    def read_json(self, filepath: Path) -> dict:
        """Read data from a JSON file.

        :param filepath: A filepath to read data from.
        :return: JSON data.
        """
        with open(filepath, mode="r", encoding=self.encoding) as f:
            json_data = json.load(f)

        return json_data

    @staticmethod
    def make_base_folder(folder: str) -> None:
        """Create a base folder.

        :param folder: A folder to create.
        :return: None.
        """
        base_folder = BaseConstants.RAW_FOLDER.joinpath(folder)

        os.makedirs(base_folder, exist_ok=True)

    @staticmethod
    def is_season_year(*, season_year: str) -> bool:
        """Check whether a specified value is a season year.

        :param season_year: A value to check.
        :return: True if the specified value is a season year.
            Otherwise, False.
        """
        match = re.fullmatch(
            pattern=SeasonConstants.SEASON_YEAR_PATTERN, string=season_year
        )

        return bool(match)
