"""Tests for the legacy and M25 Pydantic models."""

from pymadden.models import (
    M25Player,
    M25RatingsResponse,
    PlayerRating,
    RatingsResponse,
)

from .conftest import make_legacy_player, make_m25_player


def test_player_rating_model(legacy_player):
    player = PlayerRating(**legacy_player)

    assert player.firstName == "Mock"
    assert player.lastName == "Player1"
    assert player.full_name == "Mock Player1"
    assert player.position == "WR"
    assert player.overall_rating == 75
    assert "OVR 75" in str(player)


def test_player_rating_ratings_dict(legacy_player):
    player = PlayerRating(**legacy_player)
    ratings = player.ratings()

    assert ratings["speed"] == 75
    assert ratings["overall"] == 75
    # runningStyle_rating is a string and must be excluded
    assert "runningStyle" not in ratings


def test_player_rating_tolerates_new_fields(legacy_player):
    legacy_player["brandNewEAField"] = "surprise"
    player = PlayerRating(**legacy_player)
    assert player.model_dump()["brandNewEAField"] == "surprise"


def test_ratings_response_model():
    response = RatingsResponse(
        count=2, docs=[make_legacy_player(1), make_legacy_player(2)]
    )
    assert response.count == 2
    assert len(response.docs) == 2
    assert all(isinstance(doc, PlayerRating) for doc in response.docs)


def test_m25_player_model(m25_player):
    player = M25Player(**m25_player)

    assert player.full_name == "Mock Player1"
    assert player.position_id == "WR"
    assert player.team_name == "Team 1"
    assert player.overallRating == 90
    assert player.stat("speed") == 85
    assert player.stat("does-not-exist") is None
    assert player.playerAbilities[0].label == "Double Me"
    assert "OVR 90" in str(player)


def test_m25_player_flat_dict(m25_player):
    player = M25Player(**m25_player)
    flat = player.to_flat_dict()

    assert flat["fullName"] == "Mock Player1"
    assert flat["position"] == "WR"
    assert flat["team"] == "Team 1"
    assert flat["overall_rating"] == 90
    assert flat["speed_rating"] == 85
    assert flat["abilities"] == ["Double Me"]
    assert flat["iteration"] == "1-base"


def test_m25_player_flat_dict_includes_diffs(m25_player):
    m25_player["stats"]["speed"] = {"value": 88, "diff": 3}
    flat = M25Player(**m25_player).to_flat_dict()
    assert flat["speed_rating"] == 88
    assert flat["speed_diff"] == 3


def test_m25_string_stat_values(m25_player):
    m25_player["stats"]["runningStyle"] = {"value": "Default", "diff": 0}
    player = M25Player(**m25_player)
    assert player.stat("runningStyle") == "Default"


def test_m25_ratings_response():
    response = M25RatingsResponse(
        items=[make_m25_player(1), make_m25_player(2)], totalItems=1957
    )
    assert response.totalItems == 1957
    assert len(response.items) == 2
    assert all(isinstance(item, M25Player) for item in response.items)
