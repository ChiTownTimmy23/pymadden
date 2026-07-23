"""Configuration: game versions, ratings iterations, and endpoint settings."""

from __future__ import annotations

from enum import Enum


class GameVersion(str, Enum):
    """Supported Madden NFL game versions."""

    M22 = "m22"
    M23 = "m23"
    M24 = "m24"
    M25 = "m25"

    @classmethod
    def parse(cls, value: str | GameVersion) -> GameVersion:
        """Coerce a string like ``"m24"`` (case-insensitive) into a GameVersion."""
        if isinstance(value, cls):
            return value
        try:
            return cls(str(value).lower())
        except ValueError:
            options = ", ".join(v.value for v in cls)
            raise ValueError(
                f"Invalid game version {value!r}. Available options: {options}"
            ) from None

    @property
    def uses_legacy_api(self) -> bool:
        """M22-M24 share the legacy ratings-api.ea.com endpoint."""
        return self is not GameVersion.M25


class Iteration(str, Enum):
    """Ratings iterations for Madden 22-24 (legacy API)."""

    LAUNCH_RATINGS = "launch-ratings"
    WEEK_1 = "week-1"
    WEEK_2 = "week-2"
    WEEK_3 = "week-3"
    WEEK_4 = "week-4"
    WEEK_5 = "week-5"
    WEEK_6 = "week-6"
    WEEK_7 = "week-7"
    WEEK_8 = "week-8"
    WEEK_9 = "week-9"
    WEEK_10 = "week-10"
    WEEK_11 = "week-11"
    WEEK_12 = "week-12"
    WEEK_13 = "week-13"
    WEEK_14 = "week-14"
    WEEK_15 = "week-15"
    WEEK_16 = "week-16"
    WEEK_17 = "week-17"
    WEEK_18 = "week-18"
    WILD_CARD_ROUND = "wild-card-round"
    DIVISIONAL_ROUND = "divisional-round"
    CONFERENCE_CHAMPIONSHIP_ROUND = "conference-championship-round"
    PRO_BOWL = "pro-bowl"
    SUPER_BOWL = "super-bowl"


class M25Iteration(str, Enum):
    """Ratings iterations for Madden 25 (drop API).

    The drop API prefixes each iteration id with an ordinal, e.g. ``9-week-8``.
    """

    BASE = "1-base"
    WEEK_1 = "2-week-1"
    WEEK_2 = "3-week-2"
    WEEK_3 = "4-week-3"
    WEEK_4 = "5-week-4"
    WEEK_5 = "6-week-5"
    WEEK_6 = "7-week-6"
    WEEK_7 = "8-week-7"
    WEEK_8 = "9-week-8"
    WEEK_9 = "10-week-9"
    WEEK_10 = "11-week-10"
    WEEK_11 = "12-week-11"
    WEEK_12 = "13-week-12"
    WEEK_13 = "14-week-13"
    WEEK_14 = "15-week-14"
    WEEK_15 = "16-week-15"
    WEEK_17 = "18-week-17"
    WEEK_18 = "19-week-18"
    WILD_CARD_ROUND = "20-wild-card-round"
    DIVISIONAL_ROUND = "21-divisional-round"
    CONFERENCE_CHAMPIONSHIP_ROUND = "22-conference-championship-round"
    SUPER_BOWL = "23-super-bowl"


class Config:
    """Endpoint configuration for the EA ratings APIs."""

    # Madden 22-24 (legacy API)
    BASE_URL: str = "https://ratings-api.ea.com/v2/entities"
    RATINGS_PATHS: dict = {
        GameVersion.M22: "m22-ratings",
        GameVersion.M23: "m23-ratings",
        GameVersion.M24: "m24-ratings",
    }
    # NOTE: the legacy API's `page` parameter is broken (every page returns the
    # first page of results), so pagination must use `limit` + `offset`.
    LEGACY_PAGE_SIZE: int = 1000

    # Madden 25 (drop API)
    M25_BASE_URL: str = "https://drop-api.ea.com/rating/madden-nfl"
    M25_PAGE_SIZE: int = 100  # drop API rejects limits above 100

    # HTTP client defaults
    DEFAULT_TIMEOUT: float = 30.0
    DEFAULT_MAX_RETRIES: int = 3
    DEFAULT_MAX_CONCURRENCY: int = 4
    DEFAULT_REQUESTS_PER_SECOND: float = 5.0
    DEFAULT_CACHE_TTL: float = 300.0
    USER_AGENT: str = "pymadden (https://github.com/ChiTownTimmy23/pymadden)"


def validate_iteration(
    game_version: GameVersion, iteration: str | Iteration | M25Iteration
) -> str:
    """Validate an iteration for a game version and return its string value.

    :raises ValueError: if the iteration is not valid for the game version.
    """
    enum_cls = M25Iteration if game_version is GameVersion.M25 else Iteration
    raw = iteration.value if isinstance(iteration, Enum) else str(iteration)
    try:
        return enum_cls(raw).value
    except ValueError:
        options = ", ".join(i.value for i in enum_cls)
        raise ValueError(
            f"Invalid iteration {raw!r} for {game_version.value}. "
            f"Available options: {options}"
        ) from None
