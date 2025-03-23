import logging

from collectors.leagues.league_collector import LeagueCollector
from collectors.players.player_collector import PlayerCollector
from collectors.seasons.season_collector import SeasonCollector
from collectors.teams.team_collector import TeamCollector
from common.constants import (
    BaseConstants,
    ConferenceConstants,
    ConferenceStatsConstants,
    LeagueConstants,
    LoggerConstants,
    PlayerConstants,
    PlayerStatsConstants,
    SeasonConstants,
    TeamConstants,
    TeamStatsConstants,
)
from common.logger import init_logger
from extractors.conferences.conference_extractor import ConferenceExtractor
from extractors.conferences.conference_stats_extractor import (
    ConferenceStatsExtractor,
)
from extractors.players.player_extractor import PlayerExtractor
from extractors.players.player_stats_extractor import PlayerStatsExtractor
from extractors.seasons.season_extractor import SeasonExtractor
from extractors.teams.team_extractor import TeamExtractor
from extractors.teams.team_stats_extractor import TeamStatsExtractor
from uploader.uploader import Uploader


def create_base_folders(upl: Uploader) -> None:
    """Create `raw` and `processed` folders to store source and
    processed data, respectively.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(msg="Creation of the base folders has been started.")

    upl.make_base_folder(base_folder=BaseConstants.RAW_FOLDER)
    upl.make_base_folder(base_folder=BaseConstants.PROCESSED_FOLDER)

    logger.info(msg="Creation of the base folder has been completed.")


def collect_seasons(collector: SeasonCollector) -> None:
    """Collect the seasons data and save it to the appropriate
    filepath.

    :param collector: A collector that initiates the collection
    process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.SEASON_COLLECTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.SEASON_COLLECTOR_LOGGER_NAME
    )

    logger.info(msg="Data collection of seasons has been started.")

    collector.make_base_folder(folder=SeasonConstants.SEASONS_FOLDER)

    html_data = collector.get_html_data(collector.url)

    collector.save_html(
        html_data=html_data, filepath=SeasonConstants.RAW_FILEPATH
    )

    logger.info(msg="Data collection of seasons has been completed.")


def upload_collected_seasons(upl: Uploader) -> None:
    """Upload collected seasons data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading collected seasons data to an S3 bucket has been "
        "started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(
        SeasonConstants.SEASONS_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".html",),
    )

    logger.info(
        msg="Uploading collected seasons data to an S3 bucket has been "
        "completed."
    )


def extract_seasons(extractor: SeasonExtractor) -> None:
    """Extract the seasons data and save it to the appropriate
    filepath.

    :param extractor: An extractor that initiates the extraction
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.SEASON_EXTRACTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.SEASON_EXTRACTOR_LOGGER_NAME
    )

    logger.info(msg="Data extraction of seasons has been started.")

    extractor.make_base_folder(
        base_path=BaseConstants.PROCESSED_FOLDER,
        folder=SeasonConstants.SEASONS_FOLDER,
    )

    seasons_df = extractor.get_seasons_df()
    seasons_urls = extractor.get_seasons_urls()

    extractor.save_table(
        table_df=seasons_df, filepath=SeasonConstants.PROCESSED_FILEPATH
    )
    extractor.save_json(
        json_data=seasons_urls,
        filepath=SeasonConstants.SEASONS_URLS_FILEPATH,
    )

    logger.info(msg="Data extraction of seasons has been completed.")


def upload_extracted_seasons(upl: Uploader) -> None:
    """Upload extracted seasons data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading extracted seasons data to an S3 bucket has been "
        "started."
    )

    raw_base_folder = BaseConstants.RAW_FOLDER.joinpath(
        SeasonConstants.SEASONS_FOLDER
    )
    processed_base_folder = BaseConstants.PROCESSED_FOLDER.joinpath(
        SeasonConstants.SEASONS_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=raw_base_folder,
        extensions=(".json",),
    )
    upl.upload_files_to_s3(
        base_folder=processed_base_folder,
        extensions=(".parquet",),
    )

    logger.info(
        msg="Uploading extracted seasons data to an S3 bucket has been "
        "completed."
    )


def collect_leagues(collector: LeagueCollector) -> None:
    """Collect the leagues data and save it to the appropriate
    filepath.

    :param collector: A collector that initiates the collection
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.LEAGUE_COLLECTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.LEAGUE_COLLECTOR_LOGGER_NAME
    )

    logger.info(msg="Data collection of leagues has been started.")

    collector.make_base_folder(folder=LeagueConstants.LEAGUES_FOLDER)

    collector.get_leagues_html_data()

    logger.info(msg="Data collection of leagues has been completed.")


def upload_collected_leagues(upl: Uploader) -> None:
    """Upload collected leagues data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading collected leagues data to an S3 bucket has been "
        "started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(
        LeagueConstants.LEAGUES_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".html",),
    )

    logger.info(
        msg="Uploading collected leagues data to an S3 bucket has been "
        "completed."
    )


def extract_conferences(extractor: ConferenceExtractor) -> None:
    """Extract the conferences data and save it to the appropriate
    filepath.

    :param extractor: An extractor that initiates the extraction
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.CONFERENCE_EXTRACTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.CONFERENCE_EXTRACTOR_LOGGER_NAME
    )

    logger.info(msg="Data extraction of conferences has been started.")

    extractor.make_base_folder(
        base_path=BaseConstants.PROCESSED_FOLDER,
        folder=ConferenceConstants.CONFERENCES_FOLDER,
    )

    conferences_df = extractor.update_conferences_df()

    extractor.save_table(
        table_df=conferences_df,
        filepath=ConferenceConstants.PROCESSED_FILEPATH,
    )

    logger.info(msg="Data extraction of conferences has been completed.")


def upload_extracted_conferences(upl: Uploader) -> None:
    """Upload collected seasons data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading extracted conferences data to an S3 bucket has "
        "been started."
    )

    base_folder = BaseConstants.PROCESSED_FOLDER.joinpath(
        ConferenceConstants.CONFERENCES_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".parquet",),
    )

    logger.info(
        msg="Uploading extracted conferences data to an S3 bucket has "
        "been completed."
    )


def extract_conferences_stats(extractor: ConferenceStatsExtractor) -> None:
    """Extract the conferences stats data and save it to the
    appropriate filepath.

    :param extractor: An extractor that initiates the extraction
        process.
    :return: None.
    """
    init_logger(
        logger_name=LoggerConstants.CONFERENCE_STATS_EXTRACTOR_LOGGER_NAME
    )
    logger = logging.getLogger(
        name=LoggerConstants.CONFERENCE_STATS_EXTRACTOR_LOGGER_NAME
    )

    logger.info(msg="Data extraction of conferences stats has been started.")

    extractor.make_base_folder(
        base_path=BaseConstants.PROCESSED_FOLDER,
        folder=ConferenceStatsConstants.CONFERENCES_STATS_FOLDER,
    )

    conferences_stats_df = [
        extractor.get_per_game_teams_stats_df(),
        extractor.get_per_game_opponents_stats_df(),
        extractor.get_total_teams_stats_df(),
        extractor.get_total_opponents_stats_df(),
        extractor.get_per_100_possessions_teams_stats_df(),
        extractor.get_per_100_possessions_opponents_stats_df(),
        extractor.get_advanced_teams_stats_df(),
        extractor.get_shooting_teams_stats_df(),
        extractor.get_shooting_opponents_stats_df(),
    ]

    for stats_df, stats_filepath in zip(
        conferences_stats_df,
        ConferenceStatsConstants.PROCESSED_FILEPATHS,
        strict=True,
    ):
        extractor.save_table(
            table_df=stats_df,
            filepath=stats_filepath,
        )

    logger.info(msg="Data extraction of conferences stats has been completed.")


def upload_extracted_conferences_stats(upl: Uploader) -> None:
    """Upload extracted conferences stats data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading extracted conferences stats data to an S3 bucket "
        "has been started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(
        ConferenceStatsConstants.CONFERENCES_STATS_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".parquet",),
    )

    logger.info(
        msg="Uploading extracted conferences stats data to an S3 bucket "
        "has been completed."
    )


def extract_teams(extractor: TeamExtractor) -> None:
    """Extract the teams data and save it to the appropriate
    filepath.

    :param extractor: An extractor that initiates the extraction
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.TEAM_EXTRACTOR_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.TEAM_EXTRACTOR_LOGGER_NAME)

    logger.info(msg="Data extraction of teams has been started.")

    extractor.make_base_folder(
        base_path=BaseConstants.RAW_FOLDER,
        folder=TeamConstants.TEAMS_FOLDER,
    )

    teams_urls = extractor.get_teams_urls()

    extractor.save_json(
        json_data=teams_urls, filepath=TeamConstants.RAW_FILEPATH
    )

    logger.info(msg="Data extraction of teams has been completed.")


def upload_extracted_teams(upl: Uploader) -> None:
    """Upload extracted teams data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading extracted teams data to an S3 bucket has been "
        "started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(TeamConstants.TEAMS_FOLDER)

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".json",),
    )

    logger.info(
        msg="Uploading extracted teams data to an S3 bucket has been "
        "completed."
    )


def collect_teams(collector: TeamCollector) -> None:
    """Collect the teams data and save it to the appropriate
    filepath.

    :param collector: A collector that initiates the collection
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.TEAM_COLLECTOR_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.TEAM_COLLECTOR_LOGGER_NAME)

    logger.info(msg="Data collection of teams has been started.")

    collector.get_teams_html_data()

    logger.info(msg="Data collection of teams has been completed.")


def upload_collected_teams(upl: Uploader) -> None:
    """Upload collected teams data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading collected teams data to an S3 bucket has been "
        "started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(TeamConstants.TEAMS_FOLDER)

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".html",),
    )

    logger.info(
        msg="Uploading collected teams data to an S3 bucket has been "
        "completed."
    )


def extract_teams_stats(extractor: TeamStatsExtractor) -> None:
    """Extract the teams stats data and save it to the appropriate
    filepath.

    :param extractor: An extractor that initiates the extraction
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.TEAM_STATS_EXTRACTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.TEAM_STATS_EXTRACTOR_LOGGER_NAME
    )

    logger.info(msg="Data extraction of teams stats has been started.")

    extractor.make_base_folder(
        base_path=BaseConstants.PROCESSED_FOLDER,
        folder=TeamStatsConstants.TEAMS_STATS_FOLDER,
    )

    teams_stats_dfs = [
        extractor.get_rosters_df(),
        extractor.get_regular_season_per_game_stats_df(),
        extractor.get_playoffs_per_game_stats_df(),
        extractor.get_regular_season_total_stats_df(),
        extractor.get_playoffs_total_stats_df(),
        extractor.get_regular_season_per_36_minutes_stats_df(),
        extractor.get_playoffs_per_36_minutes_stats_df(),
        extractor.get_regular_season_per_100_possessions_stats_df(),
        extractor.get_playoffs_per_100_possessions_stats_df(),
        extractor.get_regular_season_advanced_stats_df(),
        extractor.get_playoffs_advanced_stats_df(),
        extractor.get_regular_season_adjusted_shooting_stats_df(),
        extractor.get_playoffs_adjusted_shooting_stats_df(),
        extractor.get_regular_season_shooting_stats_df(),
        extractor.get_playoffs_shooting_stats_df(),
        extractor.get_regular_season_play_by_play_stats_df(),
        extractor.get_playoffs_play_by_play_stats_df(),
        extractor.get_salaries_df(),
    ]

    for stats_df, stats_filepath in zip(
        teams_stats_dfs,
        TeamStatsConstants.PROCESSED_FILEPATHS,
        strict=True,
    ):
        extractor.save_table(
            table_df=stats_df,
            filepath=stats_filepath,
        )

    logger.info(msg="Data collection of teams stats has been completed.")


def upload_extracted_teams_stats(upl: Uploader) -> None:
    """Upload extracted teams stats data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading extracted teams stats data to an S3 bucket has "
        "been started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(
        TeamStatsConstants.TEAMS_STATS_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".parquet",),
    )

    logger.info(
        msg="Uploading extracted teams stats data to an S3 bucket has "
        "been completed."
    )


def extract_players(extractor: PlayerExtractor) -> None:
    """Extract the players data and save it to the appropriate
    filepath.

    :param extractor: An extractor that initiates the extraction
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.PLAYER_EXTRACTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.PLAYER_EXTRACTOR_LOGGER_NAME
    )

    logger.info(msg="Data extraction of players has been started.")

    extractor.make_base_folder(
        base_path=BaseConstants.RAW_FOLDER,
        folder=PlayerConstants.PLAYERS_FOLDER,
    )

    players_urls = extractor.get_players_urls()

    extractor.save_json(
        json_data=players_urls,
        filepath=PlayerConstants.PLAYERS_URLS_FILEPATH,
    )

    logger.info(msg="Data extraction of players has been completed.")


def upload_extracted_players(upl: Uploader) -> None:
    """Upload extracted players data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading extracted players data to an S3 bucket has been "
        "started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(
        PlayerConstants.PLAYERS_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".json",),
    )

    logger.info(
        msg="Uploading extracted players data to an S3 bucket has been "
        "completed."
    )


def collect_players(collector: PlayerCollector) -> None:
    """Collect the players data and save it to the appropriate
    filepath.

    :param collector: A collector that initiates the collection
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.PLAYER_COLLECTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.PLAYER_COLLECTOR_LOGGER_NAME
    )

    logger.info(msg="Data collection of players has been started.")

    collector.get_players_html_data()

    logger.info(msg="Data collection of players has been completed.")


def upload_collected_players(upl: Uploader) -> None:
    """Upload collected players data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading collected players data to an S3 bucket has been "
        "started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(
        PlayerConstants.PLAYERS_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".html",),
    )

    logger.info(
        msg="Uploading collected players data to an S3 bucket has been "
        "completed."
    )


def extract_players_stats(extractor: PlayerStatsExtractor) -> None:
    """Extract the players stats data and save it to the appropriate
    filepath.

    :param extractor: An extractor that initiates the extraction
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.PLAYER_STATS_EXTRACTOR_LOGGER_NAME)
    logger = logging.getLogger(
        name=LoggerConstants.PLAYER_STATS_EXTRACTOR_LOGGER_NAME
    )

    logger.info(msg="Data extraction of players stats has been started.")

    extractor.make_base_folder(
        base_path=BaseConstants.PROCESSED_FOLDER,
        folder=PlayerStatsConstants.PLAYERS_STATS_FOLDER,
    )

    players_stats_df = extractor.get_players_stats_df()

    extractor.save_table(
        table_df=players_stats_df,
        filepath=PlayerStatsConstants.PLAYERS_STATS_FILEPATH,
    )

    logger.info(msg="Data extraction of players stats has been completed.")


def upload_extracted_players_stats(upl: Uploader) -> None:
    """Upload extracted players stats data to an S3 bucket.

    :param upl: An uploader that initiates the uploading
        process.
    :return: None.
    """
    init_logger(logger_name=LoggerConstants.UPLOADER_LOGGER_NAME)
    logger = logging.getLogger(name=LoggerConstants.UPLOADER_LOGGER_NAME)

    logger.info(
        msg="Uploading extracted players data to an S3 bucket has been "
        "started."
    )

    base_folder = BaseConstants.RAW_FOLDER.joinpath(
        PlayerStatsConstants.PLAYERS_STATS_FOLDER
    )

    upl.upload_files_to_s3(
        base_folder=base_folder,
        extensions=(".parquet",),
    )

    logger.info(
        msg="Uploading extracted players data to an S3 bucket has been "
        "completed."
    )


if __name__ == "__main__":
    init_logger(logger_name=LoggerConstants.SERVICE_LOGGER_NAME)
    src_logger = logging.getLogger(name=LoggerConstants.SERVICE_LOGGER_NAME)

    uploader = Uploader()
    season_collector = SeasonCollector(url=SeasonConstants.URL)
    season_extractor = SeasonExtractor()
    league_collector = LeagueCollector()
    conference_extractor = ConferenceExtractor()
    conferences_stats_extractor = ConferenceStatsExtractor()
    team_extractor = TeamExtractor()
    team_collector = TeamCollector()
    team_stats_extractor = TeamStatsExtractor()
    player_extractor = PlayerExtractor()
    player_collector = PlayerCollector()
    player_stats_extractor = PlayerStatsExtractor()

    try:
        create_base_folders(upl=uploader)

        collect_seasons(collector=season_collector)
        upload_collected_seasons(upl=uploader)

        extract_seasons(extractor=season_extractor)
        upload_extracted_seasons(upl=uploader)

        collect_leagues(collector=league_collector)
        upload_collected_leagues(upl=uploader)

        extract_conferences(extractor=conference_extractor)
        upload_extracted_conferences(upl=uploader)

        extract_conferences_stats(extractor=conferences_stats_extractor)
        upload_extracted_conferences_stats(upl=uploader)

        extract_teams(extractor=team_extractor)
        upload_extracted_teams(upl=uploader)

        collect_teams(collector=team_collector)
        upload_collected_teams(upl=uploader)

        extract_teams_stats(extractor=team_stats_extractor)
        upload_extracted_teams_stats(upl=uploader)

        extract_players(extractor=player_extractor)
        upload_extracted_players(upl=uploader)

        collect_players(collector=player_collector)
        upload_collected_players(upl=uploader)

        extract_players_stats(extractor=player_stats_extractor)
        upload_extracted_players_stats(upl=uploader)
    except Exception as e:
        src_logger.error(msg=e)
