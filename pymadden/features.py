"""Derived player features computed from the raw ratings data.

These work on both legacy (:class:`~pymadden.models.PlayerRating`) and M25
(:class:`~pymadden.models.M25Player`) players by normalizing each into a flat
``{stat: value}`` mapping first.
"""

from __future__ import annotations

from typing import Any

from .models import M25Player, PlayerRating

Player = PlayerRating | M25Player

# Stat groups used for composite scores (legacy naming, sans "_rating").
_SPEED_SCORE_STATS = ("speed", "acceleration", "agility", "changeOfDirection")
_COVERAGE_STATS = ("manCoverage", "zoneCoverage", "press", "playRecognition")
_PASS_RUSH_STATS = ("powerMoves", "finesseMoves", "blockShedding", "pursuit")
_ROUTE_RUNNING_STATS = (
    "shortRouteRunning",
    "mediumRouteRunning",
    "deepRouteRunning",
)
_THROWING_STATS = (
    "throwPower",
    "throwAccuracyShort",
    "throwAccuracyMid",
    "throwAccuracyDeep",
    "throwOnTheRun",
    "throwUnderPressure",
)


def _numeric_ratings(player: Player) -> dict[str, float]:
    if isinstance(player, PlayerRating):
        return {name: float(value) for name, value in player.ratings().items()}
    return {
        name: float(entry.value)
        for name, entry in player.stats.items()
        if isinstance(entry.value, int | float)
    }


def _mean(ratings: dict[str, float], stats: tuple) -> float:
    values = [ratings[s] for s in stats if s in ratings]
    return round(sum(values) / len(values), 1) if values else 0.0


def _identity(player: Player) -> dict[str, Any]:
    if isinstance(player, PlayerRating):
        return {
            "id": player.primaryKey,
            "fullName": player.full_name,
            "position": player.position,
            "team": player.team,
            "overall": player.overall_rating,
            "age": player.age,
            "height": player.height,
            "weight": player.weight,
            "yearsPro": player.yearsPro,
        }
    return {
        "id": player.id,
        "fullName": player.full_name,
        "position": player.position_id,
        "team": player.team_name,
        "overall": player.overallRating,
        "age": player.age,
        "height": player.height,
        "weight": player.weight,
        "yearsPro": player.yearsPro,
    }


def derive_features(player: Player) -> dict[str, Any]:
    """Compute derived features for a single player.

    Returns the player's identity fields plus:

    - ``bmi``: body mass index from height (in) and weight (lb).
    - ``speed_score``: mean of speed, acceleration, agility, change of direction.
    - ``coverage_score``: mean of man/zone coverage, press, play recognition.
    - ``pass_rush_score``: mean of power/finesse moves, block shedding, pursuit.
    - ``route_running_score``: mean of short/medium/deep route running.
    - ``throwing_score``: mean of the six throwing ratings.
    - ``athleticism_delta``: speed_score minus overall (raw athletes score high).
    """
    ratings = _numeric_ratings(player)
    features = _identity(player)

    height = features.get("height") or 0
    weight = features.get("weight") or 0
    features["bmi"] = (
        round(703 * weight / (height**2), 1) if height and weight else None
    )

    features["speed_score"] = _mean(ratings, _SPEED_SCORE_STATS)
    features["coverage_score"] = _mean(ratings, _COVERAGE_STATS)
    features["pass_rush_score"] = _mean(ratings, _PASS_RUSH_STATS)
    features["route_running_score"] = _mean(ratings, _ROUTE_RUNNING_STATS)
    features["throwing_score"] = _mean(ratings, _THROWING_STATS)
    features["athleticism_delta"] = round(
        features["speed_score"] - (features["overall"] or 0), 1
    )
    return features


def derive_features_for_all(players: list[Player]) -> list[dict[str, Any]]:
    """Compute derived features for a list of players."""
    return [derive_features(player) for player in players]
