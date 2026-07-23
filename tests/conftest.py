"""Shared fixtures: compact builders for legacy and M25 API payloads."""

from typing import Any

import pytest

LEGACY_INT_RATINGS = [
    "awareness_rating",
    "throwPower_rating",
    "kickReturn_rating",
    "leadBlock_rating",
    "strength_rating",
    "bCVision_rating",
    "catchInTraffic_rating",
    "playAction_rating",
    "pursuit_rating",
    "mediumRouteRunning_rating",
    "catching_rating",
    "acceleration_rating",
    "spinMove_rating",
    "finesseMoves_rating",
    "spectacularCatch_rating",
    "runBlock_rating",
    "tackle_rating",
    "injury_rating",
    "zoneCoverage_rating",
    "deepRouteRunning_rating",
    "trucking_rating",
    "throwAccuracyShort_rating",
    "jukeMove_rating",
    "playRecognition_rating",
    "shortRouteRunning_rating",
    "breakSack_rating",
    "speed_rating",
    "runBlockPower_rating",
    "jumping_rating",
    "toughness_rating",
    "throwOnTheRun_rating",
    "manCoverage_rating",
    "stiffArm_rating",
    "powerMoves_rating",
    "release_rating",
    "hitPower_rating",
    "throwAccuracyMid_rating",
    "kickAccuracy_rating",
    "passBlockPower_rating",
    "impactBlocking_rating",
    "stamina_rating",
    "carrying_rating",
    "breakTackle_rating",
    "kickPower_rating",
    "throwUnderPressure_rating",
    "passBlock_rating",
    "changeOfDirection_rating",
    "press_rating",
    "throwAccuracyDeep_rating",
    "blockShedding_rating",
    "runBlockFinesse_rating",
    "agility_rating",
    "overall_rating",
    "passBlockFinesse_rating",
]

M25_STAT_NAMES = [
    "speed",
    "acceleration",
    "agility",
    "changeOfDirection",
    "overall",
    "awareness",
    "catching",
    "throwPower",
    "manCoverage",
    "zoneCoverage",
    "press",
    "playRecognition",
]


def make_legacy_player(key: int = 1, **overrides: Any) -> dict[str, Any]:
    """Build a full legacy API player document with sensible defaults."""
    player: dict[str, Any] = dict.fromkeys(LEGACY_INT_RATINGS, 75)
    player.update(
        {
            "primaryKey": key,
            "firstName": "Mock",
            "lastName": f"Player{key}",
            "fullNameForSearch": f"Mock Player{key}",
            "position": "WR",
            "team": f"Team {key}",
            "teamId": key,
            "jerseyNum": 10 + key,
            "age": 26,
            "height": 72,
            "weight": 200,
            "college": "Mock University",
            "yearsPro": 3,
            "archetype": "WR_DeepThreat",
            "iteration": "launch-ratings",
            "status": "published",
            "plyrAssetname": f"MockPlayer{key}",
            "plyrBirthdate": "2/2/1992",
            "plyrHandedness": "Right",
            "plyrPortrait": key,
            "totalSalary": 3000000,
            "signingBonus": 500000,
            "runningStyle_rating": "Default Stride Tight",
        }
    )
    player.update(overrides)
    return player


def make_m25_player(key: int = 1, **overrides: Any) -> dict[str, Any]:
    """Build a full M25 drop API player item with sensible defaults."""
    player: dict[str, Any] = {
        "id": key,
        "firstName": "Mock",
        "lastName": f"Player{key}",
        "birthdate": "2000-01-01",
        "college": "Mock University",
        "height": 72,
        "weight": 205,
        "age": 25,
        "jerseyNum": key,
        "yearsPro": 4,
        "handedness": 1,
        "avatarUrl": "https://example.com/avatar.png",
        "overallRating": 90,
        "position": {
            "id": "WR",
            "shortLabel": "WR",
            "label": "Wide Receiver",
        },
        "team": {"id": key, "label": f"Team {key}"},
        "archetype": {"id": "WR_DeepThreat", "label": "Deep Threat - WR"},
        "iteration": {"id": "1-base", "label": "Launch Ratings"},
        "stats": {name: {"value": 85, "diff": 0} for name in M25_STAT_NAMES},
        "playerAbilities": [
            {
                "id": "Z_07",
                "label": "Double Me",
                "description": "Wins contested catches.",
                "type": {"id": "xFactor", "label": "X-Factor"},
            }
        ],
    }
    player.update(overrides)
    return player


@pytest.fixture
def legacy_player() -> dict[str, Any]:
    return make_legacy_player()


@pytest.fixture
def m25_player() -> dict[str, Any]:
    return make_m25_player()
