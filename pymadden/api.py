from typing import List
from pymadden.models import RatingsResponse, PlayerRating
from pymadden.config import VALID_GAME_VERSIONS, BASE_URL
import requests


class EARatingsAPI:
    """
    A class for interacting with the EA Ratings API.
    """

    def __init__(self, game_version: str):
        """
        Initialize the EARatingsAPI instance with the specified game version.

        Args:
            game_version (str): The version of the game (e.g., "m22-ratings").

        Raises:
            ValueError: If the provided game version is invalid.
        """
        self._validate_game_version(game_version)
        self.game_version = game_version

    def _validate_game_version(self, game_version: str) -> None:
        """
        Validate the provided game version.

        Args:
            game_version (str): The version of the game.

        Raises:
            ValueError: If the provided game version is invalid.
        """
        if game_version not in VALID_GAME_VERSIONS:
            raise ValueError(
                f"Invalid game version. Allowed versions are {', '.join(VALID_GAME_VERSIONS)}."
            )

    def _validate_week_number(self, week_number: int) -> None:
        """
        Validate the provided week number.

        Args:
            week_number (int): The week number.

        Raises:
            ValueError: If the provided week number is invalid.
        """
        special_iterations = {0, 19, 20, 21, 22, 23, 79, 99}
        if not isinstance(week_number, int) or (
            week_number < 0 and week_number not in special_iterations
        ):
            raise ValueError(
                "Week number must be a non-negative integer or one of the special iterations."
            )

    def _fetch_ratings(self, iteration: str, limit: int = 1000) -> List[PlayerRating]:
        """
        Fetch player ratings for the specified iteration.

        Args:
            iteration (str): The iteration to fetch ratings for (e.g., "launch-ratings").
            limit (int): The maximum number of ratings to fetch per request.

        Returns:
            List[PlayerRating]: A list of player ratings.

        Raises:
            RatingsAPIError: If the API request fails.
        """
        offset = 0
        total_count = 0
        all_players = []

        while True:
            params = {
                "filter": f"iteration:{iteration}",
                "limit": limit,
                "offset": offset,
            }
            response = requests.get(f"{BASE_URL}{self.game_version}", params=params)

            if response.status_code == 200:
                response_data = response.json()
                total_count = response_data["count"]
                players = [PlayerRating(**player) for player in response_data["docs"]]
                all_players.extend(players)

                if offset + limit >= total_count:
                    break
                offset += limit
            else:
                raise RatingsAPIError(
                    f"Request failed with status code {response.status_code}: {response.text}"
                )

        return all_players

    def get_ratings(self, iteration: str = "launch-ratings") -> List[PlayerRating]:
        """
        Get player ratings for the specified iteration.

        Args:
            iteration (str): The iteration to fetch ratings for (e.g., "launch-ratings").

        Returns:
            List[PlayerRating]: A list of player ratings.
        """
        return self._fetch_ratings(iteration)

    def get_ratings_by_week(self, week_number: int) -> List[PlayerRating]:
        """
        Get player ratings for the specified week number.

        Args:
            week_number (int): The week number.

        Returns:
            List[PlayerRating]: A list of player ratings.

        Raises:
            ValueError: If the provided week number is invalid.
            WeekNotPlayedError: If the specified week has not been played yet.
        """
        self._validate_week_number(week_number)
        iteration = f"week-{week_number}"

        try:
            ratings = self._fetch_ratings(iteration)
        except RatingsAPIError as e:
            if "not found" in str(e):
                raise WeekNotPlayedError(f"Week {week_number} has not been played yet.")
            else:
                raise

        return ratings


class RatingsAPIError(Exception):
    """
    Custom exception class for API errors.
    """

    pass


class WeekNotPlayedError(Exception):
    """
    Custom exception class for indicating that a week has not been played yet.
    """

    pass
