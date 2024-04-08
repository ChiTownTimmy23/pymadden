from pymadden.client import EARatingsClient


def test_api_initialization():
    api = EARatingsClient("m23-ratings")
    assert api.game_version == "m23-ratings"
