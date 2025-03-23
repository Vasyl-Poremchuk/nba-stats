from pathlib import Path

from collectors.base_collector import BaseCollector
from common.constants import BaseConstants, PlayerConstants
from common.exceptions import HTMLExtensionError


class PlayerCollector(BaseCollector):
    """A class to collect data for players.

    :param encoding: The encoding of the data.
    """

    def __init__(self, encoding="utf-8") -> None:
        """Construct all necessary attributes for the `PlayerCollector`
        object.

        :param encoding: The encoding of the data.
        """
        super().__init__(encoding=encoding)

    @staticmethod
    def get_player_filepath(player_url: str) -> Path:
        """Get a filepath of the player based on the specified URL.

        :param player_url: A URL of the player.
        :return: A filepath of the player.
        """
        *_, filename = player_url.split("/")

        player, extension = filename.split(".")

        if extension != BaseConstants.RAW_FILE_EXTENSION:
            raise HTMLExtensionError(extension=extension)

        player_filepath = BaseConstants.RAW_FOLDER.joinpath(
            PlayerConstants.PLAYERS_FOLDER, filename
        )

        return player_filepath

    def get_players_html_data(self) -> None:
        """Get HTML pages (data) of the players.

        :return: None.
        """
        players_urls = self.read_json(
            filepath=PlayerConstants.PLAYERS_URLS_FILEPATH
        )

        for player_url in players_urls.values():
            player_filepath = self.get_player_filepath(player_url=player_url)
            player_html_data = self.get_html_data(url=player_url)

            self.save_html(
                html_data=player_html_data, filepath=player_filepath
            )
