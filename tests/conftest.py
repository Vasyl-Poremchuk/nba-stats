import pytest

from collectors.base_collector import BaseCollector
from collectors.leagues.league_collector import LeagueCollector
from collectors.players.player_collector import PlayerCollector
from collectors.teams.team_collector import TeamCollector
from extractors.base_extractor import BaseExtractor
from extractors.conferences.conference_extractor import ConferenceExtractor
from extractors.conferences.conference_stats_extractor import (
    ConferenceStatsExtractor,
)
from extractors.players.player_extractor import PlayerExtractor
from extractors.players.player_stats_extractor import PlayerStatsExtractor
from extractors.seasons.season_extractor import SeasonExtractor
from extractors.teams.team_extractor import TeamExtractor
from extractors.teams.team_stats_extractor import TeamStatsExtractor


@pytest.fixture
def base_collector() -> BaseCollector:
    """Create a fresh instance of `BaseCollector` before each test.

    :return: An instance of `BaseCollector`.
    """
    return BaseCollector()


@pytest.fixture
def league_collector() -> LeagueCollector:
    """Create a fresh instance of `LeagueCollector` before each test.

    :return: An instance of `LeagueCollector`.
    """
    return LeagueCollector()


@pytest.fixture
def player_collector() -> PlayerCollector:
    """Create a fresh instance of `PlayerCollector` before each test.

    :return: An instance of `PlayerCollector`.
    """
    return PlayerCollector()


@pytest.fixture
def team_collector() -> TeamCollector:
    """Create a fresh instance of `TeamCollector` before each test.

    :return: An instance of `TeamCollector`.
    """
    return TeamCollector()


@pytest.fixture
def base_extractor() -> BaseExtractor:
    """Create a fresh instance of `BaseExtractor` before each test.

    :return: An instance of `BaseExtractor`.
    """
    return BaseExtractor()


@pytest.fixture
def conference_extractor() -> ConferenceExtractor:
    """Create a fresh instance of `ConferenceExtractor` before each
    test.

    :return: An instance of `ConferenceExtractor`.
    """
    return ConferenceExtractor()


@pytest.fixture
def conference_stats_extractor() -> ConferenceStatsExtractor:
    """Create a fresh instance of `ConferenceStatsExtractor` before each
    test.

    :return: An instance of `ConferenceStatsExtractor`.
    """
    return ConferenceStatsExtractor()


@pytest.fixture
def player_extractor() -> PlayerExtractor:
    """Create a fresh instance of `PlayerExtractor` before each test.

    :return: An instance of `PlayerExtractor`.
    """
    return PlayerExtractor()


@pytest.fixture
def player_stats_extractor() -> PlayerStatsExtractor:
    """Create a fresh instance of `PlayerStatsExtractor` before each
    test.

    :return: An instance of `PlayerStatsExtractor`.
    """
    return PlayerStatsExtractor()


@pytest.fixture
def season_extractor() -> SeasonExtractor:
    """Create a fresh instance of `SeasonExtractor` before each test.

    :return: An instance of `SeasonExtractor`.
    """
    return SeasonExtractor()


@pytest.fixture
def team_extractor() -> TeamExtractor:
    """Create a fresh instance of `TeamExtractor` before each test.

    :return: An instance of `TeamExtractor`.
    """
    return TeamExtractor()


@pytest.fixture
def team_stats_extractor() -> TeamStatsExtractor:
    """Create a fresh instance of `TeamStatsExtractor` before each test.

    :return: An instance of `TeamStatsExtractor`.
    """
    return TeamStatsExtractor()
