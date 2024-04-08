import requests

class EARatingsClient:
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