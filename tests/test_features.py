"""Tests for derived player features."""

from pymadden.features import derive_features, derive_features_for_all
from pymadden.models import M25Player, PlayerRating

from .conftest import make_legacy_player, make_m25_player


def test_derive_features_legacy():
    player = PlayerRating(
        **make_legacy_player(
            1,
            speed_rating=90,
            acceleration_rating=88,
            agility_rating=86,
            changeOfDirection_rating=84,
            overall_rating=80,
            height=72,
            weight=200,
        )
    )
    features = derive_features(player)

    assert features["fullName"] == "Mock Player1"
    assert features["speed_score"] == 87.0  # mean of 90, 88, 86, 84
    assert features["athleticism_delta"] == 7.0
    assert features["bmi"] == 27.1  # 703 * 200 / 72^2


def test_derive_features_m25():
    raw = make_m25_player(1)
    raw["stats"]["speed"] = {"value": 96, "diff": 0}
    raw["stats"]["acceleration"] = {"value": 94, "diff": 0}
    raw["stats"]["agility"] = {"value": 92, "diff": 0}
    raw["stats"]["changeOfDirection"] = {"value": 90, "diff": 0}
    player = M25Player(**raw)

    features = derive_features(player)

    assert features["team"] == "Team 1"
    assert features["speed_score"] == 93.0
    assert features["overall"] == 90
    assert features["athleticism_delta"] == 3.0


def test_derive_features_skips_missing_stat_groups():
    raw = make_m25_player(1)
    raw["stats"] = {"speed": {"value": 90, "diff": 0}}
    features = derive_features(M25Player(**raw))

    assert features["speed_score"] == 90.0
    assert features["throwing_score"] == 0.0


def test_derive_features_for_all():
    players = [
        PlayerRating(**make_legacy_player(1)),
        PlayerRating(**make_legacy_player(2)),
    ]
    features = derive_features_for_all(players)
    assert len(features) == 2
    assert features[0]["id"] == 1
    assert features[1]["id"] == 2
