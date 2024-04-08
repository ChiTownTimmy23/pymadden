from pymadden.api import EARatingsAPI


def test_api_initialization():
    api = EARatingsAPI("m23-ratings")
    assert api.game_version == "m23-ratings"
