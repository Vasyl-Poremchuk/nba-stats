from pathlib import Path


class BaseConstants:
    URL = "https://www.basketball-reference.com"
    BASE_FOLDER = Path(__file__).parents[1]
    RAW_FOLDER = BASE_FOLDER.joinpath("raw")
    PROCESSED_FOLDER = BASE_FOLDER.joinpath("processed")
    RAW_FILE_EXTENSION = "html"
    TIME_SLEEP_SECONDS = 3
    MAX_WORKERS = 6


class LoggerConstants:
    COLLECTORS_LOGGER_NAME = "src.collectors"
    EXTRACTORS_LOGGER_NAME = "src.extractors"
    BASE_COLLECTOR_LOGGER_NAME = f"{COLLECTORS_LOGGER_NAME}.base_collector"
    LEAGUE_COLLECTOR_LOGGER_NAME = (
        f"{COLLECTORS_LOGGER_NAME}.leagues.league_collector"
    )
    PLAYER_COLLECTOR_LOGGER_NAME = (
        f"{COLLECTORS_LOGGER_NAME}.players.player_collector"
    )
    SEASON_COLLECTOR_LOGGER_NAME = (
        f"{COLLECTORS_LOGGER_NAME}.seasons.season_collector"
    )
    TEAM_COLLECTOR_LOGGER_NAME = (
        f"{COLLECTORS_LOGGER_NAME}.teams.team_collector"
    )
    BASE_EXTRACTOR_LOGGER_NAME = f"{EXTRACTORS_LOGGER_NAME}.base_extractor"
    CONFERENCE_EXTRACTOR_LOGGER_NAME = (
        f"{EXTRACTORS_LOGGER_NAME}.conferences.conference_extractor"
    )
    CONFERENCE_STATS_EXTRACTOR_LOGGER_NAME = (
        f"{EXTRACTORS_LOGGER_NAME}.conferences.conference_stats_extractor"
    )
    PLAYER_EXTRACTOR_LOGGER_NAME = (
        f"{EXTRACTORS_LOGGER_NAME}.players.player_extractor"
    )
    PLAYER_STATS_EXTRACTOR_LOGGER_NAME = (
        f"{EXTRACTORS_LOGGER_NAME}.players.player_stats_extractor"
    )
    SEASON_EXTRACTOR_LOGGER_NAME = (
        f"{EXTRACTORS_LOGGER_NAME}.seasons.season_extractor"
    )
    TEAM_EXTRACTOR_LOGGER_NAME = (
        f"{EXTRACTORS_LOGGER_NAME}.teams.team_extractor"
    )
    TEAM_STATS_EXTRACTOR_LOGGER_NAME = (
        f"{EXTRACTORS_LOGGER_NAME}.teams.team_stats_extractor"
    )
    UPLOADER_LOGGER_NAME = "src.uploader.uploader"
    SERVICE_LOGGER_NAME = "src.service"


class SeasonConstants:
    URL = f"{BaseConstants.URL}/leagues/"
    LEAGUE_TO_SELECT = "NBA"
    SEASON_YEAR_PATTERN = r"^(?:19\d{2}|20\d{2}|2100)$"
    SEASON_HREF_PATTERN = r"^/leagues/NBA_\d{4}\.html$"
    SEASONS_FOLDER = "seasons"
    COLUMNS_MAP = {
        "Season": "season",
        "Lg": "league",
        "Champion": "champion",
        "MVP": "mvp",
        "Rookie of the Year": "rookie_of_the_year",
        "Points": "top_performer_by_points",
        "Rebounds": "top_performer_by_rebounds",
        "Assists": "top_performer_by_assists",
        "Win Shares": "top_performer_by_win_shares",
    }
    RAW_FILEPATH = BaseConstants.RAW_FOLDER.joinpath(
        SEASONS_FOLDER, "seasons.html"
    )
    SEASONS_URLS_FILEPATH = BaseConstants.RAW_FOLDER.joinpath(
        SEASONS_FOLDER, "seasons-urls.json"
    )
    PROCESSED_FILEPATH = BaseConstants.PROCESSED_FOLDER.joinpath(
        SEASONS_FOLDER, "seasons.parquet"
    )


class LeagueConstants:
    LEAGUES_FOLDER = "leagues"


class ConferenceConstants:
    CONFERENCES_FOLDER = "conferences"
    COLUMNS_MAP = {
        "Eastern Conference": "team",
        "Western Conference": "team",
        "Team": "team",
        "W": "wins",
        "L": "losses",
        "W/L%": "wins_loss_percentage",
        "GB": "games_behind",
        "PS/G": "points_per_game",
        "PA/G": "opponent_points_per_game",
        "SRS": "simple_rating_system",
    }
    DATA_TYPES_MAP = {
        "wins": int,
        "losses": int,
        "wins_loss_percentage": float,
        "games_behind": float,
        "points_per_game": float,
        "opponent_points_per_game": float,
        "simple_rating_system": float,
    }
    PROCESSED_FILEPATH = BaseConstants.PROCESSED_FOLDER.joinpath(
        CONFERENCES_FOLDER, "conferences.parquet"
    )


class ConferenceStatsConstants:
    ADVANCED_SHOOTING_STATS_HEADER = 1
    PER_GAME_STATS_TEAM_ID = "per_game-team"
    PER_GAME_STATS_OPPONENT_ID = "per_game-opponent"
    TOTAL_STATS_TEAM_ID = "totals-team"
    TOTAL_STATS_OPPONENT_ID = "totals-opponent"
    PER_100_POSSESSIONS_STATS_TEAM_ID = "per_poss-team"
    PER_100_POSSESSIONS_STATS_OPPONENT_ID = "per_poss-opponent"
    ADVANCED_STATS_TEAM_ID = "advanced-team"
    SHOOTING_STATS_TEAM_ID = "shooting-team"
    SHOOTING_STATS_OPPONENT_ID = "shooting-opponent"
    TEAM_STATS = True
    OPPONENT_STATS = False
    STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Team": "team",
        "G": "games",
        "MP": "minutes_played",
        "FG": "field_goals",
        "FGA": "field_goal_attempts",
        "FG%": "field_goal_percentage",
        "3P": "3_point_field_goals",
        "3PA": "3_point_field_goal_attempts",
        "3P%": "3_point_field_goal_percentage",
        "2P": "2_point_field_goals",
        "2PA": "2_point_field_goal_attempts",
        "2P%": "2_point_field_goal_percentage",
        "FT": "free_throws",
        "FTA": "free_throws_attempts",
        "FT%": "free_throw_percentage",
        "ORB": "offensive_rebounds",
        "DRB": "defensive_rebounds",
        "TRB": "total_rebounds",
        "AST": "assists",
        "STL": "steals",
        "BLK": "blocks",
        "TOV": "turnovers",
        "PF": "personal_fouls",
        "PTS": "points",
    }
    ADVANCED_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Team": "team",
        "Age": "average_age",
        "W": "wins",
        "L": "losses",
        "PW": "pythagorean_wins",
        "PL": "pythagorean_losses",
        "MOV": "margin_of_victory",
        "SOS": "strength_of_schedule",
        "SRS": "simple_rating_system",
        "ORtg": "offensive_rating",
        "DRtg": "defensive_rating",
        "NRtg": "net_rating",
        "Pace": "pace_factor",
        "FTr": "free_throw_attempt_rate",
        "3PAr": "3_point_attempt_rate",
        "TS%": "true_shooting_percentage",
        # `off` -> `Offence Four Factors`
        "eFG%": "off_effective_field_goal_percentage",
        "TOV%": "off_turnover_percentage",
        "ORB%": "off_offensive_rebound_percentage",
        "FT/FGA": "off_free_throws_per_field_goal_attempt",
        # `dff` -> `Defense Four Factors`
        "eFG%.1": "dff_opponent_effective_field_goal_percentage",
        "TOV%.1": "dff_opponent_turnover_percentage",
        "DRB%": "dff_defensive_rebound_percentage",
        "FT/FGA.1": "dff_opponent_free_throws_per_field_goal_attempt",
        "Arena": "arena",
        "Attend.": "attendance",
        "Attend./G": "attendance_per_game",
    }
    SHOOTING_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Team": "team",
        "G": "games",
        "MP": "minutes_played",
        "FG%": "field_goal_percentage",
        "Dist.": "average_distance_of_field_goal_attempts",
        "2P": "2_point_field_goal_attempts_percentage",
        "0-3": "0_3_ft_field_goal_attempts_percentage",
        "3-10": "3_10_ft_field_goal_attempts_percentage",
        "10-16": "10_16_ft_field_goal_attempts_percentage",
        "16-3P": "16_ft_3_point_field_goal_attempts_percentage",
        "3P": "3_point_field_goal_attempts_percentage",
        "2P.1": "2_point_field_goal_percentage",
        "0-3.1": "0_3_ft_field_goal_percentage",
        "3-10.1": "3_10_ft_field_goal_percentage",
        "10-16.1": "10_16_ft_field_goal_percentage",
        "16-3P.1": "16_ft_3_point_field_goal_percentage",
        "3P.1": "3_point_field_goal_percentage",
        "2P.2": "2_point_assisted_field_goal_percentage",
        "3P.2": "3_point_assisted_field_goal_percentage",
        "%FGA": "field_goal_dunk_attempts_percentage",
        "Md.": "field_goal_dunk",
        "%FGA.1": "field_goal_layup_attempts_percentage",
        "Md..1": "field_goal_layup_percentage",
        "%3PA": "3_point_field_goal_from_corner_percentage",
        "3P%": "3_point_field_goal_attempts_from_corner_percentage",
        "Att.": "heave_attempts",
        "Md..2": "heaves_made",
    }
    STATS_DATA_TYPES_MAP = {"rank": int}
    ADVANCED_STATS_DATA_TYPES_MAP = {"rank": int, "wins": int, "losses": int}
    SHOOTING_STATS_DATA_TYPES_MAP = {"rank": int}
    CONFERENCES_STATS_FOLDER = "conferences_stats"
    PROCESSED_FILEPATHS = [
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "per-game-teams-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "per-game-opponents-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "total-teams-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "total-opponents-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "per-100-possessions-teams-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER,
            "per-100-possessions-opponents-stats.parquet",
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "advanced-teams-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "shooting-teams-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            CONFERENCES_STATS_FOLDER, "shooting-opponents-stats.parquet"
        ),
    ]


class TeamConstants:
    TEAM_HREF_SELECTOR = (
        f"table#{ConferenceStatsConstants.PER_GAME_STATS_TEAM_ID} "
        f"a[href^='/teams/']"
    )
    TEAMS_FOLDER = "teams"
    RAW_FILEPATH = BaseConstants.RAW_FOLDER.joinpath(
        TEAMS_FOLDER, "teams.json"
    )


class TeamStatsConstants:
    ADJUSTED_SHOOTING_STATS_HEADER = 1
    ROSTER_ID = "roster"
    REGULAR_SEASON_PER_GAME_STATS_ID = "per_game_stats"
    PLAYOFFS_PER_GAME_STATS_ID = "per_game_stats_post"
    REGULAR_SEASON_TOTAL_STATS_ID = "totals_stats"
    PLAYOFFS_TOTAL_STATS_ID = "totals_stats_post"
    REGULAR_SEASON_PER_36_MINUTES_STATS_ID = "per_minute_stats"
    PLAYOFFS_PER_36_MINUTES_STATS_ID = "per_minute_stats_post"
    REGULAR_SEASON_PER_100_POSSESSIONS_STATS_ID = "per_poss"
    PLAYOFFS_PER_100_POSSESSIONS_STATS_ID = "per_poss_post"
    REGULAR_SEASON_ADVANCED_STATS_ID = "advanced"
    PLAYOFFS_ADVANCED_STATS_ID = "advanced_post"
    REGULAR_SEASON_ADJUSTED_SHOOTING_STATS_ID = "adj_shooting"
    PLAYOFFS_ADJUSTED_SHOOTING_STATS_ID = "adj_shooting_post"
    REGULAR_SEASON_SHOOTING_STATS_ID = "shooting"
    PLAYOFFS_SHOOTING_STATS_ID = "shooting_post"
    REGULAR_SEASON_PLAY_BY_PLAY_STATS_ID = "pbp_stats"
    PLAYOFFS_PLAY_BY_PLAY_STATS_ID = "pbp_stats_post"
    SALARIES_ID = "salaries2"
    ROSTER_COLUMNS_MAP = {
        "No.": "uniform_number",
        "Player": "player",
        "Pos": "position",
        "Ht": "height",
        "Wt": "weight",
        "Birth Date": "birth_date",
        "Birth": "country_of_birth",
        "Exp": "years_experience",
        "College": "college",
    }
    STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Player": "player",
        "Age": "age",
        "Pos": "position",
        "G": "games",
        "GS": "games_started",
        "MP": "minutes_played",
        "FG": "field_goals",
        "FGA": "field_goal_attempts",
        "FG%": "field_goal_percentage",
        "3P": "3_point_field_goals",
        "3PA": "3_point_field_goal_attempts",
        "3P%": "3_point_field_goal_percentage",
        "2P": "2_point_field_goals",
        "2PA": "2_point_field_goal_attempts",
        "2P%": "2_point_field_goal_percentage",
        "eFG%": "effective_field_goal_percentage",
        "FT": "free_throws",
        "FTA": "free_throw_attempts",
        "FT%": "free_throw_percentage",
        "ORB": "offensive_rebounds",
        "DRB": "defensive_rebounds",
        "TRB": "total_rebounds",
        "AST": "assists",
        "STL": "steals",
        "BLK": "blocks",
        "TOV": "turnovers",
        "PF": "personal_fouls",
        "PTS": "points",
        "Awards": "awards",
    }
    TOTAL_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Player": "player",
        "Age": "age",
        "G": "games",
        "GS": "games_started",
        "MP": "minutes_played",
        "FG": "field_goals",
        "FGA": "field_goal_attempts",
        "FG%": "field_goal_percentage",
        "3P": "3_point_field_goals",
        "3PA": "3_point_field_goal_attempts",
        "3P%": "3_point_field_goal_percentage",
        "2P": "2_point_field_goals",
        "2PA": "2_point_field_goal_attempts",
        "2P%": "2_point_field_goal_percentage",
        "eFG%": "effective_field_goal_percentage",
        "FT": "free_throws",
        "FTA": "free_throw_attempts",
        "FT%": "free_throw_percentage",
        "ORB": "offensive_rebounds",
        "DRB": "defensive_rebounds",
        "TRB": "total_rebounds",
        "AST": "assists",
        "STL": "steals",
        "BLK": "blocks",
        "TOV": "turnovers",
        "PF": "personal_fouls",
        "PTS": "points",
        "Trp-Dbl": "triple_doubles",
        "Awards": "awards",
    }
    PER_100_POSSESSIONS_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Player": "player",
        "Age": "age",
        "G": "games",
        "GS": "games_started",
        "MP": "minutes_played",
        "FG": "field_goals",
        "FGA": "field_goal_attempts",
        "FG%": "field_goal_percentage",
        "3P": "3_point_field_goals",
        "3PA": "3_point_field_goal_attempts",
        "3P%": "3_point_field_goal_percentage",
        "2P": "2_point_field_goals",
        "2PA": "2_point_field_goal_attempts",
        "2P%": "2_point_field_goal_percentage",
        "eFG%": "effective_field_goal_percentage",
        "FT": "free_throws",
        "FTA": "free_throw_attempts",
        "FT%": "free_throw_percentage",
        "ORB": "offensive_rebounds",
        "DRB": "defensive_rebounds",
        "TRB": "total_rebounds",
        "AST": "assists",
        "STL": "steals",
        "BLK": "blocks",
        "TOV": "turnovers",
        "PF": "personal_fouls",
        "PTS": "points",
        "ORtg": "offensive_rating",
        "DRtg": "defensive_rating",
        "Awards": "awards",
    }
    ADVANCED_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Player": "player",
        "Age": "age",
        "Pos": "position",
        "G": "games",
        "GS": "games_started",
        "MP": "minutes_played",
        "PER": "player_efficiency_rating",
        "TS%": "true_shooting_percentage",
        "3PAr": "3_point_attempt_rate",
        "FTr": "free_throw_attempt_rate",
        "ORB%": "offensive_rebound_percentage",
        "DRB%": "defensive_rebound_percentage",
        "TRB%": "total_rebound_percentage",
        "AST%": "assist_percentage",
        "STL%": "steal_percentage",
        "BLK%": "block_percentage",
        "TOV%": "turnovers_percentage",
        "USG%": "usage_percentage",
        "OWS": "offensive_win_shares",
        "DWS": "defensive_win_shares",
        "WS": "win_shares",
        "WS/48": "win_shares_per_48_minutes",
        "OBPM": "offensive_box_plus_minus",
        "DBPM": "defensive_box_plus_minus",
        "BPM": "box_plus_minus",
        "VORP": "value_over_replacement_player",
        "Awards": "awards",
    }
    ADJUSTED_SHOOTING_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Player": "player",
        "Age": "age",
        "Pos": "position",
        "G": "games",
        "GS": "games_started",
        "MP": "minutes_played",
        "FG%": "field_goal_percentage",
        "2P%": "2_point_field_goal_percentage",
        "3P%": "3_point_field_goal_percentage",
        "eFG%": "effective_field_goal_percentage",
        "FT%": "free_throw_percentage",
        "TS%": "true_shooting_percentage",
        "FTr": "free_throw_attempt_rate",
        "3PAr": "3_point_attempt_rate",
        "FG+": "adjusted_field_goal",
        "2P+": "adjusted_2_point_field_goal",
        "3P+": "adjusted_3_point_field_goal",
        "eFG+": "adjusted_effective_field_goal",
        "FT+": "adjusted_free_throw",
        "TS+": "adjusted_true_shooting",
        "FTr+": "adjusted_free_throw_attempt",
        "3PAr+": "adjusted_3_point_attempt",
        "FG Add": "points_added_by_field_goal_shooting",
        "TS Add": "points_added_by_overall_shooting",
        "Awards": "awards",
    }
    SHOOTING_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Player": "player",
        "Age": "age",
        "Pos": "position",
        "G": "games",
        "GS": "games_started",
        "MP": "minutes_played",
        "FG%": "field_goal_percentage",
        "Dist.": "average_distance_of_field_goal_attempts",
        "2P": "2_point_field_goal_attempts_percentage",
        "0-3": "0_3_ft_field_goal_attempts_percentage",
        "3-10": "3_10_ft_field_goal_attempts_percentage",
        "10-16": "10_16_ft_field_goal_attempts_percentage",
        "16-3P": "16_ft_3_point_field_goal_attempts_percentage",
        "3P": "3_point_field_goal_attempts_percentage",
        "2P.1": "2_point_field_goal_percentage",
        "0-3.1": "0_3_ft_field_goal_percentage",
        "3-10.1": "3_10_ft_field_goal_percentage",
        "10-16.1": "10_16_ft_field_goal_percentage",
        "16-3P.1": "16_ft_3_point_field_goal_percentage",
        "3P.1": "3_point_field_goal_percentage",
        "2P.2": "2_point_assisted_field_goal_percentage",
        "3P.2": "3_point_assisted_field_goal_percentage",
        "%FGA": "field_goal_dunk_attempts_percentage",
        "#": "number_of_made_dunk_attempts",
        "%3PA": "3_point_field_goal_from_corner_percentage",
        "3P%": "3_point_field_goal_attempts_from_corner_percentage",
        "Att.": "heave_attempts",
        "Md.": "heaves_made",
        "Awards": "awards",
    }
    PLAY_BY_PLAY_STATS_COLUMNS_MAP = {
        "Rk": "rank",
        "Player": "player",
        "Age": "age",
        "Pos": "position",
        "G": "games",
        "GS": "games_started",
        "MP": "minutes_played",
        "PG%": "point_guard_percentage",
        "SG%": "shooting_guard_percentage",
        "SF%": "small_forward_percentage",
        "PF%": "power_forward_percentage",
        "C%": "center_percentage",
        "OnCourt": "plus_minus_per_100_possessions_on_court",
        "On-Off": "plus_minus_net_per_100_possessions",
        "BadPass": "turnovers_by_bad_pass",
        "LostBall": "lost_ball_turnovers",
        "Shoot": "shooting_fouls",
        "Off.": "offensive_fouls",
        "Shoot.1": "shooting_fouls_drawn",
        "Off..1": "offensive_fouls_drawn",
        "PGA": "point_generated_by_assists",
        "And1": "fouled_field_goals",
        "Blkd": "blocked_field_goal_attempts",
        "Awards": "awards",
    }
    SALARIES_COLUMNS_MAP = {
        "Rk": "rank",
        "Unnamed: 1": "player",
        "Salary": "salary",
    }
    TEAMS_STATS_FOLDER = "teams_stats"
    ROSTER_DATA_TYPES_MAP = {"uniform_number": str, "years_experience": str}
    PROCESSED_FILEPATHS = [
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "rosters.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "regular-season-per-game-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-per-game-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "regular-season-total-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-total-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "regular-season-per-36-minutes-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-per-36-minutes-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER,
            "regular-season-per-100-possessions-stats.parquet",
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-per-100-possessions-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "regular-season-advanced-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-advanced-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER,
            "regular-season-adjusted-shooting-stats.parquet",
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-adjusted-shooting-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "regular-season-shooting-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-shooting-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "regular-season-play-by-play-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "playoffs-play-by-play-stats.parquet"
        ),
        BaseConstants.PROCESSED_FOLDER.joinpath(
            TEAMS_STATS_FOLDER, "salaries.parquet"
        ),
    ]


class PlayerConstants:
    PLAYER_HREF_SELECTOR = "a[href^='/players/']"
    PLAYERS_FOLDER = "players"
    PLAYERS_URLS_FILEPATH = BaseConstants.RAW_FOLDER.joinpath(
        PLAYERS_FOLDER, "players-urls.json"
    )


class PlayerStatsConstants:
    PLAYER_H1_SELECTOR = "div#meta h1 span"
    KEYWORDS = {
        "shooting_hand": "Shoots",
        "high_schools": "High School",
        "draft": "Draft",
        "nba_debut": "NBA Debut",
    }
    STEP = 2
    DRAFT_PATTERN = r"\d+"
    PLAYER_STATS_COLUMNS = [
        "player",
        "shooting_hand",
        "high_schools",
        "picked_team",
        "draft_round",
        "draft_pick",
        "overall_draft_pick",
        "draft_year",
        "nba_debut",
    ]
    PLAYERS_STATS_FOLDER = "players_stats"
    PLAYERS_STATS_FILEPATH = BaseConstants.PROCESSED_FOLDER.joinpath(
        PLAYERS_STATS_FOLDER, "players-stats.parquet"
    )
