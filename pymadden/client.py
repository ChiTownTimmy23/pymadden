import requests


class EARatingsClient:
    """
    A client for interacting with the EA Ratings API.

    This class provides methods to retrieve rating information for a specific
    game version and iteration from the EA Ratings API.

    Args:
        game_version (str): The version of the game for which to retrieve ratings.

    Attributes:
        BASE_URL (str): The base URL of the EA Ratings API.
        game_version (str): The version of the game for which to retrieve ratings.

    Methods:
        _make_request(iteration: str) -> dict:
            Makes a request to the EA Ratings API for the specified
            game version and iteration.
            Returns the JSON response if the request is successful,
            otherwise raises an exception.
    """

    BASE_URL = "https://ratings-api.ea.com/v2/entities/"

    def __init__(self, game_version: str):
        self.game_version = game_version

    def _make_request(self, iteration: str) -> dict:
        url = f"{self.BASE_URL}{self.game_version}?filter=iteration:{iteration}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Request failed with status code {response.status_code}")
