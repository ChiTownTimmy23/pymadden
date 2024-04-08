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
        if not isinstance(week_number, int) or (week_number < 0 and week_number not in [0, 19, 20, 21, 22, 23, 79, 99]):
            raise ValueError("Week number must be a non-negative integer or one of the special iterations.")

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

        # Check for special iterations based on the week number
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

        if week_number in special_iterations:
            iteration = special_iterations[week_number]
        else:
            iteration = f"week-{week_number}"

        return self._make_request(iteration)
