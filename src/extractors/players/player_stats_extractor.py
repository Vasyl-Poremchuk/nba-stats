import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from common.constants import (
    BaseConstants,
    PlayerConstants,
    PlayerStatsConstants,
)
from extractors.base_extractor import BaseExtractor


@dataclass
class Draft:
    """A class to represent all specs of a player's draft.

    :param picked_team: A team that picked a player.
    :param draft_round: A round of the draft a player was selected
        (either `1st` or `2nd`).
    :param draft_pick: A draft number when a player was selected in the
        corresponding round.
    :param overall_draft_pick: An overall draft number when a player was
        selected.
    :param draft_year: A draft year.
    """

    picked_team: str | None = None
    draft_round: int | None = None
    draft_pick: int | None = None
    overall_draft_pick: int | None = None
    draft_year: int | None = None


class PlayerStatsExtractor(BaseExtractor):
    """A class to extract data for players stats.

    :param header: An index of the table columns.
    """

    def __init__(self, header: int = 0) -> None:
        """Construct all attributes for the `PlayerStatsExtractor`
        object.

        :param header: An index of the table columns.
        """
        super().__init__(header=header)

    def get_players_filepaths(self) -> list[Path]:
        """Get filepaths of the players.

        :return: Filepaths.
        """
        base_folder = BaseConstants.RAW_FOLDER.joinpath(
            PlayerConstants.PLAYERS_FOLDER
        )

        filepaths = self.get_filepaths(base_folder=base_folder)

        players_filepaths = [
            player_filepath
            for player_filepath in filepaths
            if player_filepath.suffix == ".html"
        ]

        return players_filepaths

    @staticmethod
    def get_player_p_tag(
        soup: BeautifulSoup, *, keyword: str, selector: str = "div#meta p"
    ) -> str | None:
        """Get a `p` tag of the player from the HTML data.

        :param soup: HTML data to extract the `p` tag from.
        :param keyword: A keyword to identify the tag.
        :param selector: CSS selector.
        :return: Player's tag value.
        """
        p_tags = soup.select(selector=selector)

        for p_tag in p_tags:
            p_tag_txt = p_tag.text.strip()

            if keyword in p_tag_txt:
                return p_tag_txt

    @staticmethod
    def get_player(soup: BeautifulSoup) -> str:
        """Get a player's name and surname from the HTML data.

        :param soup: HTML data to extract player from.
        :return: Player's name and surname.
        """
        player = soup.select_one(
            selector=PlayerStatsConstants.PLAYER_H1_SELECTOR
        ).text.strip()

        return player

    def get_shooting_hand(self, soup: BeautifulSoup) -> str | None:
        """Get a shooting hand of the player from the HTML data.

        :param soup: HTML data to extract shooting hand from.
        :return: Shooting hand.
        """
        keyword = PlayerStatsConstants.KEYWORDS.get("shooting_hand")

        p_tag_txt = self.get_player_p_tag(soup=soup, keyword=keyword)

        if not p_tag_txt:
            return None

        shooting_hand = p_tag_txt.split(":")[-1].strip().lower()

        return shooting_hand

    @staticmethod
    def group_high_schools(values: list[str]) -> list[str]:
        """Group high schools by their names and locations.

        :param values: List of values to group by.
        :return: Grouped list of high schools.
        """
        grouped_high_schools = [
            ", ".join(values[idx : idx + PlayerStatsConstants.STEP])
            for idx in range(0, len(values), PlayerStatsConstants.STEP)
        ]

        return grouped_high_schools

    def get_high_schools(self, soup: BeautifulSoup) -> str | None:
        """Get a list of high schools of the player from the HTML data.

        :param soup: HTML data to extract high schools from.
        :return: High schools.
        """
        keyword = PlayerStatsConstants.KEYWORDS.get("high_schools")

        p_tag_txt = self.get_player_p_tag(soup=soup, keyword=keyword)

        if not p_tag_txt:
            return None

        values = p_tag_txt.split(":")[-1].strip().split(", ")
        grouped_high_schools = self.group_high_schools(values=values)

        high_schools = "; ".join(
            grouped_high_school for grouped_high_school in grouped_high_schools
        )

        return high_schools

    @staticmethod
    def extract_num_value(value: str, *, idx: int = 0) -> int | None:
        """Extract a number from the specified value.

        Examples:

            - `1st round` -> 1.
            - `46th overall)` -> 46.
            - `2021 NBA Draft` -> 2021.

        :param value: A value from which to extract.
        :param idx: An index of value to extract.
        :return: Number.
        """
        values = re.findall(PlayerStatsConstants.DRAFT_PATTERN, value)

        if not values:
            return None

        num_value = int(values[idx])

        return num_value

    @staticmethod
    def get_draft_value(values: list[str], keyword: str) -> str | None:
        """Get a draft value by keyword from the HTML data.

        :param values: List of values from which to extract.
        :param keyword: A keyword to find a draft value.
        :return: Draft value.
        """
        for value in values:
            if keyword in value.lower():
                return value

    def get_draft(self, soup: BeautifulSoup) -> Draft:
        """Get draft specs of the player from the HTML data.

        :param soup: HTML data to extract draft specs from.
        :return: Draft specs.
        """
        keyword = PlayerStatsConstants.KEYWORDS.get("draft")

        p_tag_txt = self.get_player_p_tag(soup=soup, keyword=keyword)

        if not p_tag_txt:
            return Draft()

        values = p_tag_txt.split(":")[-1].strip().split(", ")

        picked_team = values[0]
        draft_round = self.get_draft_value(values=values, keyword="round")
        draft_pick = self.get_draft_value(values=values, keyword="pick")
        overall_draft_pick = self.get_draft_value(
            values=values, keyword="overall"
        )
        draft_year = self.get_draft_value(values=values, keyword="draft")

        if draft_round:
            draft_round = self.extract_num_value(value=draft_round)

        if draft_pick:
            draft_pick = self.extract_num_value(value=draft_pick, idx=1)

        if overall_draft_pick:
            overall_draft_pick = self.extract_num_value(
                value=overall_draft_pick
            )

        if draft_year:
            draft_year = self.extract_num_value(value=draft_year)

        draft_specs = Draft(
            picked_team=picked_team,
            draft_round=draft_round,
            draft_pick=draft_pick,
            overall_draft_pick=overall_draft_pick,
            draft_year=draft_year,
        )

        return draft_specs

    @staticmethod
    def extract_nba_debut(
        nba_debut_txt: str, *, fmt: str = "%B %d, %Y"
    ) -> date:
        """Extract NBA debut from the text value.

        :param nba_debut_txt: A value from which to extract NBA debut.
        :param fmt: Format of datetime to use.
        :return: NBA debut.
        """
        nba_debut = datetime.strptime(nba_debut_txt, fmt).date()

        return nba_debut

    def get_nba_debut(self, soup: BeautifulSoup) -> date | None:
        """Get NBA debut of the player from the HTML data.

        :param soup: HTML data to extract NBA debut from.
        :return: NBA debut.
        """
        keyword = PlayerStatsConstants.KEYWORDS.get("nba_debut")

        p_tag_txt = self.get_player_p_tag(soup=soup, keyword=keyword)

        if not p_tag_txt:
            return None

        nba_debut_txt = p_tag_txt.split(":")[-1].replace("*", "").strip()

        nba_debut = self.extract_nba_debut(nba_debut_txt=nba_debut_txt)

        return nba_debut

    def get_stats_df(self, player_filepath: Path) -> pd.DataFrame:
        """Get a dataframe of stats.

        :param player_filepath: Path the player file.
        :return: Stats dataframe.
        """
        html_data = self.read_html(filepath=player_filepath)
        soup = self.get_soup(html_data=html_data)

        player = self.get_player(soup=soup)
        shooting_hand = self.get_shooting_hand(soup=soup)
        high_schools = self.get_high_schools(soup=soup)

        draft = self.get_draft(soup=soup)
        picked_team = draft.picked_team
        draft_round = draft.draft_round
        draft_pick = draft.draft_pick
        overall_draft_pick = draft.overall_draft_pick
        draft_year = draft.draft_year

        nba_debut = self.get_nba_debut(soup=soup)

        data = [
            [
                player,
                shooting_hand,
                high_schools,
                picked_team,
                draft_round,
                draft_pick,
                overall_draft_pick,
                draft_year,
                nba_debut,
            ]
        ]

        stats_df = pd.DataFrame(
            data=data,
            columns=PlayerStatsConstants.PLAYER_STATS_COLUMNS,
        )

        return stats_df

    def get_players_stats_df(self) -> pd.DataFrame:
        """Get a dataframe of players stats.

        :return: Player stats dataframe.
        """
        players_filepaths = self.get_players_filepaths()

        players_stats_df = self.process_files(
            func=self.get_stats_df,
            filepaths=players_filepaths,
        )

        return players_stats_df
