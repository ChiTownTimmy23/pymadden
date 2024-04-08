# api.py
from typing import List
from pymadden.models import RatingsResponse, PlayerRating
from pymadden.config import VALID_GAME_VERSIONS, BASE_URL
import requests

class EARatingsAPI:
    def __init__(self, game_version: str):
        self._validate_game_version(game_version)
        self.game_version = game_version

    def _validate_game_version(self, game_version: str) -> None:
        if game_version not in VALID_GAME_VERSIONS:
            raise ValueError(
                f"Invalid game version. Allowed versions are {', '.join(VALID_GAME_VERSIONS)}."
            )

    def _validate_week_number(self, week_number: int) -> None:
        if not isinstance(week_number, int) or (
            week_number < 0 and week_number not in [0, 19, 20, 21, 22, 23, 79, 99]
        ):
            raise ValueError(
                "Week number must be a non-negative integer or one of the special iterations."
            )

    def _fetch_ratings(self, iteration: str, limit: int = 1000) -> List[PlayerRating]:
        offset = 0
        total_count = 0
        all_players = []

        while True:
            url = f"{BASE_URL}{self.game_version}?filter=iteration:{iteration}&limit={limit}&offset={offset}"
            response = requests.get(url)

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
                    f"Request failed with status code {response.status_code}")

        return all_players

    def get_ratings(self, iteration: str = "launch-ratings") -> List[PlayerRating]:
        return self._fetch_ratings(iteration)

    def get_ratings_by_week(self, week_number: int) -> List[PlayerRating]:
        self._validate_week_number(week_number)

        special_iterations = {
            0: "launch-ratings",
            19: "wild-card-round",
            20: "divisional-round",
            21: "conference-championship-round",
            22: "super-bowl",
            23: "pro-bowl",
            79: "rookie-ratings",
            99: "99-club",
        }

        iteration = special_iterations.get(week_number, f"week-{week_number}")
        return self._fetch_ratings(iteration)

class RatingsAPIError(Exception):
    """Custom exception class for API errors."""
    pass