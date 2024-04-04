# ea_ratings_api/api.py
import requests

from pymadden.models import RatingsResponse


class EARatingsAPI:
    BASE_URL = "https://ratings-api.ea.com/v2/entities/"
    VALID_GAME_VERSIONS = ["m21-ratings", "m22-ratings", "m23-ratings", "m24-ratings"]

    def __init__(self, game_version: str):
        self._validate_game_version(game_version)
        self.game_version = game_version

    def _validate_game_version(self, game_version: str) -> None:
        if game_version not in self.VALID_GAME_VERSIONS:
            raise ValueError(
                f"Invalid game version. Allowed versions are {', '.join(self.VALID_GAME_VERSIONS)}."
            )

    def _validate_week_number(self, week_number: int) -> None:
        if not isinstance(week_number, int) or week_number < 1:
            raise ValueError("Week number must be a positive integer.")

    def _make_request(self, iteration: str) -> RatingsResponse:
        url = f"{self.BASE_URL}{self.game_version}?filter=iteration:{iteration}"
        response = requests.get(url)

        if response.status_code == 200:
            return RatingsResponse(**response.json())
        else:
            raise Exception(f"Request failed with status code {response.status_code}")

    def get_ratings(self, iteration: str = "launch-ratings") -> RatingsResponse:
        return self._make_request(iteration)

    def get_ratings_by_week(self, week_number: int) -> RatingsResponse:
        self._validate_week_number(week_number)
        iteration = f"week-{week_number}"
        return self._make_request(iteration)
