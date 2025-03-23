from string import digits, punctuation, whitespace

from common.constants import BaseConstants, PlayerConstants, TeamConstants
from extractors.base_extractor import BaseExtractor


class PlayerExtractor(BaseExtractor):
    """A class to extract data for players.

    :param header: An index of the table columns.
    """

    def __init__(self, header: int = 0) -> None:
        """Construct all attributes for the `PlayerExtractor` object.

        :param header: An index of the table columns.
        """
        super().__init__(header=header)

    @staticmethod
    def is_player(*, player: str) -> bool:
        """Check whether a player name is valid.

        Examples:

            - `Walt Davis` -> True.
            - `...` -> False.
            - `123!` -> False.
            - `   ` -> False.

        :param player: Player name to check.
        :return: True if player name is valid, False otherwise.
        """
        excluded_characters = set(digits + punctuation + whitespace)

        is_true = not excluded_characters.issuperset(set(player))

        return is_true

    def get_players_urls(self) -> dict[str, set[str]]:
        """Get URLs of the players.

        :return: URLs.
        """
        base_folder = BaseConstants.RAW_FOLDER.joinpath(
            TeamConstants.TEAMS_FOLDER
        )

        filepaths = self.get_filepaths(base_folder=base_folder)

        players_urls = {}

        for filepath in filepaths:
            html_data = self.read_html(filepath=filepath)
            soup = self.get_soup(html_data=html_data)

            for tag in soup.select(
                selector=PlayerConstants.PLAYER_HREF_SELECTOR
            ):
                player = tag.text.strip()

                if not self.is_player(player=player) or players_urls.get(
                    player
                ):
                    continue

                href = tag.attrs.get("href")

                if not href.endswith(BaseConstants.RAW_FILE_EXTENSION):
                    continue

                player_url = BaseConstants.URL + href

                players_urls[player] = player_url

        return players_urls
