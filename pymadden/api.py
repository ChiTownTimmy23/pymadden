from pymadden.models import RatingsResponse
from pymadden.client import EARatingsClient

class EARatingsAPI:
    VALID_GAME_VERSIONS = ["m21-ratings", "m22-ratings", "m23-ratings", "m24-ratings"]

    def __init__(self, game_version: str):
        self._validate_game_version(game_version)
        self.client = EARatingsClient(game_version)

    def _validate_game_version(self, game_version: str) -> None:
        if game_version not in self.VALID_GAME_VERSIONS:
            raise ValueError(
                f"Invalid game version. Allowed versions are {', '.join(self.VALID_GAME_VERSIONS)}."
            )

    def _validate_week_number(self, week_number: int) -> None:
        if not isinstance(week_number, int) or (week_number < 0 and week_number not in [0, 19, 20, 21, 22, 23, 79, 99]):
            raise ValueError("Week number must be a non-negative integer or one of the special iterations.")

    def get_ratings(self, iteration: str = "launch-ratings") -> RatingsResponse:
        response_data = self.client._make_request(iteration)
        return RatingsResponse(**response_data)

    def get_ratings_by_week(self, week_number: int) -> RatingsResponse:
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
        response_data = self.client._make_request(iteration)
        return RatingsResponse(**response_data)